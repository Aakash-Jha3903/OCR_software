# cheques/choices.py
from django.db.models import TextChoices

class ChequeStatus(TextChoices):
    UPLOADED = "UPLOADED", "Uploaded"
    OCR_COMPLETE = "OCR_COMPLETE", "OCR Complete"
    ACCOUNT_FOUND = "ACCOUNT_FOUND", "Account Found"
    FIELD_MISMATCH = "FIELD_MISMATCH", "Field Mismatch"
    SIGN_PENDING = "SIGN_PENDING", "Signature Pending"
    SIGN_MATCH = "SIGN_MATCH", "Signature Match"
    SIGN_MISMATCH = "SIGN_MISMATCH", "Signature Mismatch"
    DEBIT_SUCCESS = "DEBIT_SUCCESS", "Debit Success"
    DEBIT_FAILED = "DEBIT_FAILED", "Debit Failed"

class Decision(TextChoices):
    PASS = "PASS", "Pass"
    FAIL = "FAIL", "Fail"
    MANUAL = "MANUAL", "Manual Review"
