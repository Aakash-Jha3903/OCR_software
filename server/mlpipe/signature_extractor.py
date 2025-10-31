import cv2
import numpy as np

def extract_signature_flexible(img_path, debug=False):
    img_color = cv2.imread(img_path)
    if img_color is None:
        raise FileNotFoundError(f"Image not found: {img_path}")
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    h_img, w_img = img_gray.shape

    # search bottom region (flexible)
    bottom_start = int(h_img * 0.55)
    cheque_bottom = img_gray[bottom_start:h_img, :]

    blur = cv2.GaussianBlur(cheque_bottom, (5,5), 0)
    enhanced = cv2.equalizeHist(blur)
    thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 17, 5)

    kernel = np.ones((3,3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    thresh = cv2.dilate(thresh, kernel, iterations=1)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    total_area = h_img * w_img
    candidates = []
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        abs_y = y + bottom_start
        if area < total_area*0.001 or area > total_area*0.20:
            continue
        aspect = w / float(h) if h > 0 else 0
        if not (1.0 <= aspect <= 12.0):
            continue
        extent = area / float(w*h) if w*h > 0 else 0
        if extent > 0.65:
            continue
        density = cv2.countNonZero(thresh[y:y+h, x:x+w]) / float(w*h) if w*h>0 else 0
        if not (0.05 <= density <= 0.65):
            continue
        vertical_bias = (abs_y + h/2) / float(h_img)
        score = (area/total_area) * (1 - extent) * (1 - abs(density - 0.35)) * vertical_bias
        candidates.append((score, x, y, w, h, abs_y))

    if not candidates:
        # fallback to bottom crop
        crop_fallback = cv2.resize(img_gray[bottom_start:h_img, :], (224,224))
        if debug:
            cv2.imshow("Fallback Signature", crop_fallback); cv2.waitKey(0); cv2.destroyAllWindows()
        return crop_fallback

    candidates.sort(reverse=True, key=lambda x: x[0])
    _, x, y, w, h, abs_y = candidates[0]

    y1 = max(0, abs_y - int(h*0.2))
    y2 = min(h_img, abs_y + h + int(h*0.2))
    x1 = max(0, x - int(w*0.1))
    x2 = min(w_img, x + w + int(w*0.1))

    signature_crop = img_gray[y1:y2, x1:x2]
    signature_crop = cv2.resize(signature_crop, (224,224))
    signature_crop = cv2.medianBlur(signature_crop, 3)

    if debug:
        debug_img = img_color.copy()
        cv2.rectangle(debug_img, (x1,y1),(x2,y2),(0,255,0),2)
        cv2.imshow("Detected Signature", debug_img)
        cv2.imshow("Cropped Signature", signature_crop)
        cv2.waitKey(0); cv2.destroyAllWindows()

    return signature_crop

