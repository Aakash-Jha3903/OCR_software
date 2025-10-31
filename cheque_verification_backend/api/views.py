from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import cv2
import numpy as np
import re
from datetime import datetime
from paddleocr import PaddleOCR, draw_ocr
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)

FONT_PATH = "C:/Windows/Fonts/arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = None


class UploadChequeView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def extract_fields(self, txts, boxes, scores, img):
        """Extract account number and amount digits from OCR output."""
        H, W = img.shape[:2]
        y_means = [np.mean([pt[1] for pt in b]) for b in boxes]
        x_means = [np.mean([pt[0] for pt in b]) for b in boxes]

        # -------- ACCOUNT NUMBER DETECTION --------
        account = None
        for i, t in enumerate(txts):
            if "Ac" in t or "A/c" in t or "Acct" in t:
                for j in range(i + 1, min(i + 4, len(txts))):
                    cand = re.sub(r'\D', '', txts[j])
                    if re.fullmatch(r'\d{9,20}', cand):
                        account = cand
                        break
            if account:
                break

        if not account:
            nums = []
            for i, t in enumerate(txts):
                for n in re.findall(r'\d{9,20}', t):
                    nums.append((n, y_means[i]))
            if nums:
                nums.sort(key=lambda x: (x[1], len(x[0])), reverse=True)
                account = nums[0][0]

        # -------- AMOUNT DETECTION --------
        amount_digits = None
        for t in txts:
            if "₹" in t or "Rs" in t:
                m = re.search(r"\d[\d,]{0,10}", t.replace(",", ""))
                if m:
                    amount_digits = m.group(0)
                    break

        if not amount_digits:
            candidates = []
            for i, t in enumerate(txts):
                m = re.search(r"\b\d{2,9}\b", t.replace(",", ""))
                if m:
                    candidates.append((m.group(0), x_means[i]))
            if candidates:
                candidates.sort(key=lambda x: x[1], reverse=True)
                amount_digits = candidates[0][0]

        if amount_digits:
            amount_digits = amount_digits.replace(",", "")

        return {
            "account_number": account or "Not Detected",
            "amount_digits": amount_digits or "Not Detected"
        }

    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({"error": "No image uploaded!"}, status=400)

        # Convert image file to numpy array
        img_arr = np.frombuffer(image.read(), np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        if img is None:
            return Response({"error": "Failed to process image!"}, status=400)

        # Run OCR
        results = ocr.ocr(img, cls=True)
        ocr_list = results[0] if results and len(results) > 0 else []
        boxes = [el[0] for el in ocr_list]
        txts = [el[1][0] for el in ocr_list]
        scores = [float(el[1][1]) for el in ocr_list]

        full_text = " ".join(txts)

        # Extract structured fields
        fields = self.extract_fields(txts, boxes, scores, img)

        # Compute OCR stats
        confidence_avg = float(np.mean(scores)) if scores else 0.0
        total_words = len(txts)
        extracted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        metadata = {
            "confidence_avg": round(confidence_avg, 4),
            "total_words": total_words,
            "extracted_at": extracted_at
        }

        # Draw OCR boxes
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_show = draw_ocr(image_rgb, boxes, txts, scores, font_path=FONT_PATH)
        im_show_resized = cv2.resize(im_show, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)

        # Convert to base64
        fig, ax = plt.subplots(figsize=(20, 6))
        ax.imshow(im_show_resized)
        ax.axis("off")
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode("utf-8")

        # Construct final response
        response_data = {
            "fields": fields,
            "metadata": metadata,
            "ocr_image": img_str,
            "full_text": full_text
        }

        return Response(response_data)


from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import cv2
import numpy as np
from .signature_verifier import verify_signatures  # Importing signature verification function

class VerifySignaturesView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # Get the uploaded cheque images
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')

        if not image1 or not image2:
            return Response({"error": "Both cheque images must be uploaded!"}, status=400)

        # Convert the images to numpy arrays
        img_arr1 = np.frombuffer(image1.read(), np.uint8)
        img1 = cv2.imdecode(img_arr1, cv2.IMREAD_COLOR)
        img_arr2 = np.frombuffer(image2.read(), np.uint8)
        img2 = cv2.imdecode(img_arr2, cv2.IMREAD_COLOR)

        if img1 is None or img2 is None:
            return Response({"error": "Failed to process images!"}, status=400)

        # Use the verify_signatures function from the signature_verifier.py
        matched, match_percent = verify_signatures(img1, img2)

        # Return the result (whether matched or not, and the similarity percentage)
        return Response({"matched": matched, "match_percent": match_percent})
