# mlpipe/signature_extractor.py
import cv2
import numpy as np

def extract_signature_flexible(image_path: str, debug: bool=False):
    """
    Return a cropped signature image (numpy array, BGR) from the cheque.
    This is a simple bottom-strip heuristic. Replace with your YOLO crop if you like.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot read {image_path}")
    h, w = img.shape[:2]
    crop = img[int(h*0.55):h, 0:w]  # bottom ~45%
    if debug:
        dbg = crop.copy()
        cv2.rectangle(img, (0, int(h*0.55)), (w, h), (0,255,0), 2)
    return crop
