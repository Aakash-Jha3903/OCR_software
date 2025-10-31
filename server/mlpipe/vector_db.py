import os
import chromadb
from signature_extractor import extract_signature_flexible
from embedding_generator import get_signature_embedding

def build_embeddings(dataset_path: str, chroma_dir: str = "chroma_db_folder"):
    client = chromadb.PersistentClient(path=chroma_dir)
    name = "cheque_signatures"
    try:
        collection = client.get_collection(name=name)
    except Exception:
        collection = client.create_collection(name=name)

    files = [os.path.join(dataset_path, f) for f in os.listdir(dataset_path)
             if f.lower().endswith((".png",".jpg",".jpeg"))]

    for p in files:
        try:
            sig = extract_signature_flexible(p, debug=False)
            emb = get_signature_embedding(sig).tolist()
            collection.add(embeddings=[emb], metadatas=[{"file_name": os.path.basename(p)}], ids=[os.path.basename(p)])
            print(f"[INFO] embedded: {p}")
        except Exception as e:
            print(f"[ERROR] {p}: {e}")

if __name__ == "__main__":
    # run manually, never during web import
    DATASET = os.getenv("EMBED_DATASET_DIR", "dataset/yolo x image")
    build_embeddings(DATASET)
