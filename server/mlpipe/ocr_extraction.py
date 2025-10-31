# mlpipe/ocr_extraction.py
# Keep this file import-safe. No top-level execution; only functions.

def extract_text_from_cheque(image_path: str) -> dict:
    """
    Input: absolute file path of the uploaded cheque image.
    Output: dict with keys used by DRF service:
      account_number (str), amount_digits (float), payee (str),
      micr (str), date_text (str)
    """
    # Try PaddleOCR first (if installed) else fall back gracefully.
    try:
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang="en")
        # ... run OCR on `image_path` and parse your regions ...
        # NOTE: Replace the following mock with your parsing logic
        result = {
            "account_number": "",   # fill from OCR
            "amount_digits": 0.0,  # fill from OCR
            "payee": "",
            "micr": "",
            "date_text": "",
        }
        result["raw"] = {"engine": "paddleocr"}
        return result
    except Exception:
        # Fallback: keep structure so the rest of pipeline doesn’t break
        return {
            "account_number": "",
            "amount_digits": 0.0,
            "payee": "",
            "micr": "",
            "date_text": "",
            "raw": {"engine": "fallback", "note": "paddleocr not available"},
        }
