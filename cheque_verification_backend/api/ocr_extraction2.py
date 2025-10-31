import os
import re
import json
import cv2
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from paddleocr import PaddleOCR, draw_ocr

# ---------------- CONFIG ----------------
IMAGE_PATH = "dataset/filled_cheque.jpg"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)

FONT_PATH = "C:/Windows/Fonts/arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = None


# ---------------- UTILS ----------------
def safe_read_image(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {path}")
    return img


def old_extractor_and_visualize(image_path, results, save_prefix):
    ocr_list = results[0] if results and len(results) > 0 else []
    boxes = [el[0] for el in ocr_list]
    txts = [el[1][0] for el in ocr_list]
    scores = [float(el[1][1]) for el in ocr_list]

    raw_text = " ".join(txts)   # ✅ keep for processing (but NOT in final JSON)

    # ----- cheque with boxes -----
    orig = safe_read_image(image_path)
    im_show = draw_ocr(orig.copy(), boxes, txts, scores, font_path=FONT_PATH)
    cheque_out = os.path.join(OUTPUT_DIR, f"{save_prefix}_cheque_with_boxes.png")
    cv2.imwrite(cheque_out, im_show)

    # ----- text columns -----
    lines = []
    for i, (t, s) in enumerate(zip(txts, scores), start=1):
        disp = re.sub(r'\s+', ' ', t.strip())
        lines.append((f"{i}. {disp}", float(s)))

    mid = (len(lines) + 1) // 2
    col1 = lines[:mid]
    col2 = lines[mid:]

    col_gap = 300
    left_margin = 60
    top_margin = 60
    line_height = 44
    col_width = 700

    num_rows = max(len(col1), len(col2))
    img_h = top_margin + num_rows * line_height + 80
    img_w = left_margin + col_width * 2 + col_gap

    text_img = np.ones((img_h, img_w, 3), dtype=np.uint8) * 255
    font = cv2.FONT_HERSHEY_SIMPLEX

    y = top_margin
    for txt_line, _ in col1:
        cv2.putText(text_img, txt_line, (left_margin, y), font, 0.78, (0, 0, 0), 2)
        y += line_height

    x2 = left_margin + col_width + col_gap
    y = top_margin
    for txt_line, _ in col2:
        cv2.putText(text_img, txt_line, (x2, y), font, 0.78, (0, 0, 0), 2)
        y += line_height

    text_out = os.path.join(OUTPUT_DIR, f"{save_prefix}_text_columns.png")
    cv2.imwrite(text_out, text_img)

    return raw_text, boxes, txts, scores


def improved_structured_extractor(raw_text, boxes, txts, scores, image_path):

    img = safe_read_image(image_path)
    H, W = img.shape[:2]

    y_means = [np.mean([pt[1] for pt in b]) for b in boxes]
    x_means = [np.mean([pt[0] for pt in b]) for b in boxes]

    # ---------------- ACCOUNT NUMBER ----------------
    account = None
    for i, t in enumerate(txts):
        if "Ac" in t or "A/c" in t or "Acct" in t:
            for j in range(i+1, min(i+4, len(txts))):
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

    # ---------------- AMOUNT DIGITS ----------------
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
        "account_number": account,
        "amount_digits": amount_digits
    }

def main():

    results = ocr.ocr(IMAGE_PATH, cls=True)

    raw_text, boxes, txts, scores = old_extractor_and_visualize(
        IMAGE_PATH, results, "old"
    )

    fields = improved_structured_extractor(raw_text, boxes, txts, scores, IMAGE_PATH)

    confidence_avg = float(np.mean(scores)) if len(scores) else 0.0
    total_words = len(txts)
    extracted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ✅ raw_text REMOVED from JSON
    final_json = {
        "fields": fields,
        "metadata": {
            "confidence_avg": round(confidence_avg, 4),
            "total_words": int(total_words),
            "extracted_at": extracted_at
        }
    }

    json_path = os.path.join(OUTPUT_DIR, "cheque_extraction_result.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=2, ensure_ascii=False)

    print("\n✅ FINAL JSON:")
    print(json.dumps(final_json, indent=2, ensure_ascii=False))

    # ---------------- SUMMARY IMAGE ----------------
    summary_img = np.ones((200, 900, 3), dtype=np.uint8) * 255
    font = cv2.FONT_HERSHEY_SIMPLEX

    lines = [
        f"Account Number : {fields.get('account_number') or 'N/A'}",
        f"Amount (digits): {fields.get('amount_digits') or 'N/A'}",
        f"Confidence Avg : {round(confidence_avg, 4)}",
        f"Total Words    : {total_words}"
    ]

    y = 40
    for L in lines:
        cv2.putText(summary_img, L, (30, y), font, 0.9, (0,0,0), 2)
        y += 40

    summary_path = os.path.join(OUTPUT_DIR, "new_extraction_summary.png")
    cv2.imwrite(summary_path, summary_img)
    print(f"✅ Saved summary → {summary_path}")


if __name__ == "__main__":
    main()
