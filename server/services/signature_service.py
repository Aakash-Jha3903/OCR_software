# services/signature_service.py
from .logger import logger
import numpy as np
import cv2

def _safe_read(img_in):
    """
    Accepts either a numpy array (already-cropped signature) or a file path.
    Returns grayscale np.ndarray.
    """
    if isinstance(img_in, np.ndarray):
        img = img_in
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img
    # assume path
    img = cv2.imread(str(img_in), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image not found: {img_in}")
    return img

def _fallback_signature_crop(img_path_or_arr):
    """
    If mlpipe.extract_signature_flexible is unavailable or fails,
    do a simple bottom-region crop that often contains signature on Indian cheques.
    """
    try:
        img = _safe_read(img_path_or_arr)
        h, w = img.shape[:2]
        y1 = int(h * 0.60)                 # bottom 40%
        crop = img[y1:h, :]
        crop = cv2.resize(crop, (224, 224))
        return crop
    except Exception as e:
        logger.exception("Fallback crop failed")
        raise e

def _fallback_embedding(gray_img):
    """
    Lightweight embedding:
      - Hu moments (7)
      - 32-bin intensity histogram
      - 32-bin edge (Canny) histogram
    Produces a ~71-dim vector, L2-normalized.
    """
    try:
        # Ensure 224x224
        if gray_img.shape[:2] != (224, 224):
            gray_img = cv2.resize(gray_img, (224, 224))

        # Hu moments (log-scaled)
        m = cv2.moments(gray_img)
        hu = cv2.HuMoments(m).flatten()
        hu = np.sign(hu) * np.log1p(np.abs(hu))

        # Intensity histogram
        hist = cv2.calcHist([gray_img], [0], None, [32], [0, 256]).flatten()
        hist = hist / (np.linalg.norm(hist) + 1e-8)

        # Edge histogram
        edges = cv2.Canny(gray_img, 50, 150)
        ehist = cv2.calcHist([edges], [0], None, [32], [0, 256]).flatten()
        ehist = ehist / (np.linalg.norm(ehist) + 1e-8)

        vec = np.concatenate([hu, hist, ehist]).astype(np.float32)
        vec = vec / (np.linalg.norm(vec) + 1e-8)
        return vec
    except Exception:
        logger.exception("Fallback embedding failed")
        return np.zeros((71,), dtype=np.float32)

def _cosine_similarity(v1, v2) -> float:
    v1 = np.asarray(v1, dtype=np.float32)
    v2 = np.asarray(v2, dtype=np.float32)
    denom = (np.linalg.norm(v1) * np.linalg.norm(v2)) + 1e-8
    return float(np.dot(v1, v2) / denom)

class SignatureService:
    """
    Signature compare with graceful degradation:
      1) Try mlpipe.extract_signature_flexible + mlpipe.get_signature_embedding
      2) If unavailable, use fallback crop + fallback embedding (OpenCV only)
    Returns similarity as percentage (0–100).
    """

    @staticmethod
    def compare_signatures(cheque_img_path: str, db_signature_path: str) -> float:
        sig_cheque = None
        sig_db = None

        # --- Try mlpipe extraction ---
        use_mlpipe = True
        try:
            from mlpipe.signature_extractor import extract_signature_flexible
        except Exception:
            use_mlpipe = False
            logger.info("mlpipe.signature_extractor not available; using fallback crop")

        if use_mlpipe:
            try:
                sig_cheque = extract_signature_flexible(cheque_img_path)
            except Exception:
                logger.exception("extract_signature_flexible failed on cheque; using fallback crop")
                sig_cheque = _fallback_signature_crop(cheque_img_path)
            try:
                # For DB signature images that already are signatures, extractor still works,
                # but fallback to raw if it raises.
                sig_db = extract_signature_flexible(db_signature_path)
            except Exception:
                logger.exception("extract_signature_flexible failed on DB signature; using fallback crop")
                sig_db = _fallback_signature_crop(db_signature_path)
        else:
            sig_cheque = _fallback_signature_crop(cheque_img_path)
            sig_db = _fallback_signature_crop(db_signature_path)

        # --- Try mlpipe embedding ---
        use_embed = True
        try:
            from mlpipe.embedding_generator import get_signature_embedding
        except Exception:
            use_embed = False
            logger.info("mlpipe.get_signature_embedding not available; using fallback embedding")

        if use_embed:
            try:
                emb1 = get_signature_embedding(sig_cheque)
                emb2 = get_signature_embedding(sig_db)
            except Exception:
                logger.exception("mlpipe embedding failed; using fallback embedding")
                emb1 = _fallback_embedding(_safe_read(sig_cheque))
                emb2 = _fallback_embedding(_safe_read(sig_db))
        else:
            emb1 = _fallback_embedding(_safe_read(sig_cheque))
            emb2 = _fallback_embedding(_safe_read(sig_db))

        sim = _cosine_similarity(emb1, emb2)
        pct = round(sim * 100.0, 2)
        logger.info(f"Signature similarity={pct}%")
        return pct
