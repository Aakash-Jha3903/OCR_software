import cv2
import numpy as np
from signature_extractor import extract_signature_flexible
from embedding_generator import get_signature_embedding

# ---------- Helper: Compute cosine similarity ----------
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# ---------- Main verification pipeline ----------
def verify_signatures(img_path1, img_path2, threshold=0.80, debug=False):
    # 1️⃣ Extract signatures from both images
    sig1 = extract_signature_flexible(img_path1, debug=debug)
    sig2 = extract_signature_flexible(img_path2, debug=debug)

    # 2️⃣ Generate embeddings using your ResNet model
    emb1 = get_signature_embedding(sig1)
    emb2 = get_signature_embedding(sig2)

    # 3️⃣ Compute similarity
    similarity = cosine_similarity(emb1, emb2)
    match_percent = similarity * 100

    # 4️⃣ Print & return result
    print(f"Signature Similarity: {match_percent:.2f}%")

    if similarity >= threshold:
        print("✅ Verified: Signatures Match")
        return True, match_percent
    else:
        print("❌ Not Verified: Signatures Do Not Match")
        return False, match_percent


# ---------- Example Run ----------
if __name__ == "__main__":
    img1 = "dataset/yolo x image/9968.jpg"
    img2 = "Signature/50.jpg"

    verify_signatures(img1, img2, threshold=0.80, debug=True)


