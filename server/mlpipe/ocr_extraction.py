import re
import os
import cv2
import matplotlib.pyplot as plt
from paddleocr import PaddleOCR
# draw_ocr location — import from utils.visual to avoid ModuleNotFoundError
from paddleocr import draw_ocr

# Initialize OCR (set use_gpu=False on most local Windows machines)
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
# ...existing code...


# Load cheque image
image_path = "dataset/yolo x image/1.jpg"   # <-- replace with your cheque image
results = ocr.ocr(image_path, cls=True)

# Store extracted text
all_text = []
for line in results[0]:
    _, (text, confidence) = line
    print(f"Detected: {text} (Confidence: {confidence:.2f})")
    all_text.append(text)

full_text = " ".join(all_text)



# ---------- Extract cheque fields ----------
cheque_data = {}

# Date (matches 12/09/2025, 12-09-25, etc.)
date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', full_text)
if date_match:
    cheque_data["Date"] = date_match.group(1)

# Amount in digits (₹12345 or 12345.00)
amount_digits_match = re.search(r'₹?\s?\d{2,9}(\.\d{1,2})?', full_text)
if amount_digits_match:
    cheque_data["Amount (digits)"] = amount_digits_match.group(0)

# Amount in words (simple heuristic: look for "Rupees" till "only")
amount_words_match = re.search(r'Rupees(.*?)only', full_text, re.IGNORECASE)
if amount_words_match:
    cheque_data["Amount (words)"] = amount_words_match.group(0)

# MICR line (usually long digits at bottom, 9–18 chars)
micr_match = re.search(r'\b\d{9,18}\b', full_text)
if micr_match:
    cheque_data["MICR"] = micr_match.group(0)

# Payee (look for "Pay to" or nearest text after "Pay")
payee_match = re.search(r'Pay(.*?)\d', full_text)  # crude pattern
if payee_match:
    cheque_data["Payee"] = payee_match.group(1).strip()

# --- Example OCR Results (yours will be real) ---
ocr = PaddleOCR(use_angle_cls=True, lang='en')
results = ocr.ocr(image_path)

# Extract text info
boxes = [elements[0] for elements in results[0]]
txts = [elements[1][0] for elements in results[0]]
scores = [elements[1][1] for elements in results[0]]

# Visualize with font path
image = cv2.imread(image_path)
im_show = draw_ocr(
    image,
    boxes,
    txts,
    scores,
    font_path="C:/Windows/Fonts/arial.ttf"
)

# Resize for better visibility (optional)
scale_percent = 200  # increase to 200% size
width = int(im_show.shape[1] * scale_percent / 100)
height = int(im_show.shape[0] * scale_percent / 100)
dim = (width, height)
im_show_resized = cv2.resize(im_show, dim, interpolation=cv2.INTER_LINEAR)

# Display
plt.figure(figsize=(20, 6))  # make figure wider
plt.imshow(cv2.cvtColor(im_show_resized, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()

