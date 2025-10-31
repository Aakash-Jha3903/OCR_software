# import chromadb
# from signature_extractor import extract_signature_flexible
# from embedding_generator import get_signature_embedding
# import os

# # 1️⃣ Initialize Chroma client (new API)
# client = chromadb.Client()  # default local client

# # 2️⃣ Create or get collection
# collection_name = "cheque_signatures"
# existing_collections = [col.name for col in client.list_collections()]

# if collection_name in existing_collections:
#     collection = client.get_collection(name=collection_name)
# else:
#     collection = client.create_collection(name=collection_name)

# # 3️⃣ Process all cheque images
# dataset_path = "dataset/yolo x image"
# image_files = [os.path.join(dataset_path, f) for f in os.listdir(dataset_path)
#                if f.lower().endswith((".png", ".jpg", ".jpeg"))]

# for img_path in image_files:
#     try:
#         sig_crop = extract_signature_flexible(img_path, debug=False)
#         embedding = get_signature_embedding(sig_crop).tolist()
#         metadata = {"file_name": os.path.basename(img_path)}

#         collection.add(
#             embeddings=[embedding],
#             metadatas=[metadata],
#             ids=[os.path.basename(img_path)]
#         )

#         print(f"[INFO] Processed: {img_path}")

#     except Exception as e:
#         print(f"[ERROR] {img_path}: {str(e)}")

# print("[INFO] All embeddings stored successfully in ChromaDB.")


import chromadb
from signature_extractor import extract_signature_flexible
from embedding_generator import get_signature_embedding
import os

# ✅ Initialize persistent ChromaDB client
client = chromadb.PersistentClient(path="chroma_db_folder")

# ✅ Create or get collection
collection_name = "cheque_signatures"
existing_collections = [col.name for col in client.list_collections()]

if collection_name in existing_collections:
    collection = client.get_collection(name=collection_name)
else:
    collection = client.create_collection(name=collection_name)

# ✅ Process all cheque images
dataset_path = "dataset/yolo x image"
image_files = [os.path.join(dataset_path, f) for f in os.listdir(dataset_path)
               if f.lower().endswith((".png", ".jpg", ".jpeg"))]

for img_path in image_files:
    try:
        sig_crop = extract_signature_flexible(img_path, debug=False)
        embedding = get_signature_embedding(sig_crop).tolist()
        metadata = {"file_name": os.path.basename(img_path)}

        collection.add(
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[os.path.basename(img_path)]
        )

        print(f"[INFO] Processed: {img_path}")

    except Exception as e:
        print(f"[ERROR] {img_path}: {str(e)}")

print("[✅] All embeddings stored successfully in 'chroma_db_folder/'.")





