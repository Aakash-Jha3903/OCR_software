from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import cv2
import numpy as np
from paddleocr import PaddleOCR, draw_ocr  # <-- Import the draw_ocr function
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)  # Force CPU usage

class UploadChequeView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # Get the uploaded image file
        image = request.FILES.get('image')

        if not image:
            return Response({"error": "No image uploaded!"}, status=400)

        # Convert the image file to numpy array
        img_arr = np.frombuffer(image.read(), np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

        if img is None:
            return Response({"error": "Failed to process image!"}, status=400)

        # Perform OCR on the image
        results = ocr.ocr(img, cls=True)

        # Extract the text and confidence from the OCR results
        all_text = []
        for line in results[0]:
            _, (text, confidence) = line
            all_text.append(text)

        full_text = " ".join(all_text)

        # Extract specific fields from the OCR text using regex (e.g., date, amount, payee)
        cheque_data = {}
        # Add regex extraction here (same as the previous example for date, amount, payee, etc.)

        # Display OCR results using Matplotlib
        boxes = [elements[0] for elements in results[0]]
        txts = [elements[1][0] for elements in results[0]]
        scores = [elements[1][1] for elements in results[0]]

        # Convert the image to RGB before drawing
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

        # Visualize the OCR results
        im_show = draw_ocr(image_rgb, boxes, txts, scores, font_path="C:/Windows/Fonts/arial.ttf")

        # Resize for better visibility (optional)
        scale_percent = 200  # increase to 200% size
        width = int(im_show.shape[1] * scale_percent / 100)
        height = int(im_show.shape[0] * scale_percent / 100)
        dim = (width, height)
        im_show_resized = cv2.resize(im_show, dim, interpolation=cv2.INTER_LINEAR)

        # Convert to RGB for Matplotlib (this step is done already with cvtColor)
        im_show_rgb = cv2.cvtColor(im_show_resized, cv2.COLOR_BGR2RGB)

        # Plot the image with Matplotlib
        fig, ax = plt.subplots(figsize=(20, 6))
        ax.imshow(im_show_rgb)
        ax.axis("off")

        # Convert the Matplotlib plot to an image to send to frontend
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        print("Full OCR Text:", full_text)

        # Return the image as base64 string along with extracted text
        return Response({"cheque_data": cheque_data, "full_text": full_text, "ocr_image": img_str})


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
