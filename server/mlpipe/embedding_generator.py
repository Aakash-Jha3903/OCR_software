# import torch
# import torch.nn as nn
# from torchvision import models, transforms
# from PIL import Image

# # Device
# device = "cuda" if torch.cuda.is_available() else "cpu"

# # Pretrained ResNet18 model
# resnet = models.resnet18(pretrained=True)
# resnet.fc = nn.Identity()  # Remove classification head
# resnet = resnet.to(device)
# resnet.eval()

# # Preprocessing
# preprocess = transforms.Compose([
#     transforms.ToPILImage(),
#     transforms.Grayscale(num_output_channels=3),  # ResNet expects 3 channels
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406],
#                          std=[0.229, 0.224, 0.225])
# ])

# def get_signature_embedding(signature_img):
#     """
#     Generate a normalized embedding (512-dim) for a signature image
#     """
#     img_tensor = preprocess(signature_img).unsqueeze(0).to(device)
#     with torch.no_grad():
#         embedding = resnet(img_tensor)
#     embedding = embedding / embedding.norm(dim=-1, keepdim=True)
#     return embedding.cpu().numpy()[0]

import cv2
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array
from signature_extractor import extract_signature_flexible  # your extractor

# 1️⃣ Load pretrained CNN for feature extraction
base_model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg", input_shape=(224,224,3))
feature_extractor = Model(inputs=base_model.input, outputs=base_model.output)

# 2️⃣ Prepare signature image for CNN
def prepare_signature_image(img):
    """
    Converts grayscale image to RGB, normalizes, adds batch dimension.
    Input: img (H x W) grayscale
    Output: 1 x 224 x 224 x 3 numpy array
    """
    if len(img.shape) == 2:  # grayscale
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img = cv2.resize(img, (224,224))
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# 3️⃣ Generate embedding
def get_signature_embedding(signature_crop, detected_region=None):
    """
    signature_crop: 224x224 cropped grayscale signature
    detected_region: optional, thresholded/preprocessed region
    Returns: 1D embedding vector
    """
    crop_img = prepare_signature_image(signature_crop)

    if detected_region is not None:
        detected_img = prepare_signature_image(detected_region)
        emb_crop = feature_extractor.predict(crop_img, verbose=0)[0]
        emb_detected = feature_extractor.predict(detected_img, verbose=0)[0]
        embedding = (emb_crop + emb_detected) / 2.0
    else:
        embedding = feature_extractor.predict(crop_img, verbose=0)[0]

    return embedding

# # 4️⃣ Example usage
# if __name__ == "__main__":
#     img_path = "Signature/image.png"
#     # Extract signature
#     cropped_sig = extract_signature_flexible(img_path, debug=True)

#     # Generate embedding
#     embedding = get_signature_embedding(cropped_sig, detected_region=cropped_sig)

#     print("Embedding shape:", embedding.shape)
#     print("Sample embedding values:", embedding[:10])

