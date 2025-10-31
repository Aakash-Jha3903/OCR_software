# services/verification_service.py
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from core.models import Account
from cheques.models import Cheque, Verification
from .ocr_service import OCRService
from .signature_service import SignatureService
from cheques.choices import ChequeStatus, Decision
from .logger import logger

class VerificationService:

    @staticmethod
    def verify_cheque(cheque: Cheque, *, sign_threshold: float | None = None) -> Verification:
        v = Verification.objects.create(cheque=cheque)
        logger.info(f"Verify start cheque_id={cheque.id}")

        ocr = OCRService.run_ocr(cheque.image.path)
        if "error" in ocr:
            v.message = ocr["error"]
            v.decision = Decision.FAIL
            v.finished_at = timezone.now()
            v.save()
            cheque.status = ChequeStatus.FIELD_MISMATCH
            cheque.save()
            return v

        cheque.date_text = ocr.get("date_text") or ""
        cheque.payee = (ocr.get("payee") or "").upper()
        cheque.amount_digits = Decimal(str(ocr.get("amount_digits", 0)))
        cheque.micr = ocr.get("micr") or ""
        cheque.ocr_raw = ocr["raw"]
        cheque.status = ChequeStatus.OCR_COMPLETE
        cheque.save()

        # Account lookup (prefer account number; fallback MICR prefix)
        acc = None
        acct_no = (ocr.get("account_number") or "").strip()
        if acct_no:
            acc = Account.objects.filter(account_number=acct_no, is_active=True).first()
        if not acc and cheque.micr:
            acc = Account.objects.filter(bank__micr_prefix__startswith=cheque.micr[:5], is_active=True).first()

        if not acc:
            v.is_account_found = False
            v.decision = Decision.FAIL
            v.message = "Account not found."
            v.finished_at = timezone.now()
            v.save()
            cheque.status = ChequeStatus.FIELD_MISMATCH
            cheque.save()
            return v

        v.is_account_found = True
        cheque.detected_account = acc
        cheque.status = ChequeStatus.ACCOUNT_FOUND
        cheque.save()

        # Field match: in India, payee often equals holder (self cheque). You can relax as needed.
        matched = True
        if cheque.payee and cheque.payee not in acc.holder_name.upper():
            matched = False
        v.are_core_fields_matched = matched
        if not matched:
            v.decision = Decision.FAIL
            v.message = "Payee name mismatch."
            v.finished_at = timezone.now()
            v.save()
            cheque.status = ChequeStatus.FIELD_MISMATCH
            cheque.save()
            return v

        cheque.status = ChequeStatus.SIGN_PENDING
        cheque.save()

        if sign_threshold is not None:
            v.sign_threshold = float(sign_threshold)

        similarity = SignatureService.compare_signatures(cheque.image.path, acc.signature_image.path)
        v.sign_similarity = similarity

        if similarity < v.sign_threshold:
            v.decision = Decision.FAIL
            v.message = f"Signature mismatch ({similarity}%)."
            v.finished_at = timezone.now()
            v.save()
            cheque.status = ChequeStatus.SIGN_MISMATCH
            cheque.save()
            return v

        cheque.status = ChequeStatus.SIGN_MATCH
        cheque.save()

        # Atomic debit with row lock to prevent double spend
        amount = cheque.amount_digits or Decimal("0")
        with transaction.atomic():
            acc_locked = Account.objects.select_for_update().get(pk=acc.pk)
            if amount <= 0:
                v.decision = Decision.FAIL
                v.message = "Invalid cheque amount."
                cheque.status = ChequeStatus.DEBIT_FAILED
            elif amount > acc_locked.balance:
                v.decision = Decision.FAIL
                v.message = "Insufficient balance."
                cheque.status = ChequeStatus.DEBIT_FAILED
            else:
                acc_locked.balance -= amount
                acc_locked.save()
                v.debit_amount = amount
                v.debit_post_balance = acc_locked.balance
                v.decision = Decision.PASS
                v.message = f"Cheque cleared. ₹{amount} debited."
                cheque.status = ChequeStatus.DEBIT_SUCCESS

        v.finished_at = timezone.now()
        v.save()
        cheque.save()
        logger.info(f"Verify end cheque_id={cheque.id} decision={v.decision}")
        return v
