# services/ocr_service.py
import os
from .logger import logger

class OCRService:
    @staticmethod
    def run_ocr(image_path: str):
        # QUICK STUB for end-to-end testing:
        if os.getenv("USE_OCR_STUB", "1") == "1":
        # if os.getenv("USE_OCR_STUB", "0") == "1":
            logger.info("Using OCR STUB")
            return {
                "account_number": "1234567890",
                "amount_digits": 5000.0,
                "payee": "RAVI KUMAR",
                "date_text": "2025-10-30",
                "micr": "002123456",
                "raw": {"_stub": True}
            }

        try:
            from mlpipe.ocr_extraction import extract_text_from_cheque
        except Exception as e:
            return {"error": f"OCR import failed: {e}"}

        try:
            data = extract_text_from_cheque(image_path)
            logger.info(f"OCR ok for {image_path}")
        except Exception as e:
            return {"error": f"OCR failed: {e}"}

        return {
            "account_number": (data.get("account_number") or "").strip(),
            "amount_digits": float(data.get("amount_digits", 0) or 0),
            "payee": (data.get("payee") or "").strip(),
            "date_text": data.get("date") or data.get("date_text"),
            "micr": (data.get("micr") or "").strip(),
            "raw": data,
        }
