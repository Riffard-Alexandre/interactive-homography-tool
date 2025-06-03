"""
Batch Homography Transformer
----------------------------

Applies a manually defined homography transformation to a folder of input images,
aligning them to match a reference image (e.g., SWIR) using warpPerspective.

Author: Riffard Alexandre
GitHub: https://github.com/Riffard-Alexandre/interactive-homography-tool
License: MIT
"""


import cv2
import numpy as np
import os
from pathlib import Path

# === Paramètres manuels récupérés depuis l'outil interactif ===
tx = -669.0
ty = -532.0
theta = -1.0  # en degrés
scale = 2.0
persp_x = 0.0
persp_y = 0.0

# === Dossiers ===
input_folder = "input_images"       # dossier contenant les images à transformer
output_folder = "output_images"     # dossier de sortie (sera créé si inexistant)
reference_image = "swir.png"        # image de référence pour connaître les dimensions

# Créer le dossier de sortie si besoin
os.makedirs(output_folder, exist_ok=True)

# Charger l'image de référence pour connaître la taille finale
ref_img = cv2.imread(reference_image)
if ref_img is None:
    raise FileNotFoundError(f"Reference image '{reference_image}' not found.")
height, width = ref_img.shape[:2]

# Calcul de la matrice d'homographie
def build_homography_matrix(tx, ty, theta_deg, scale, persp_x, persp_y):
    theta_rad = np.deg2rad(theta_deg)

    # Matrices de transformation
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0, 1]], dtype=np.float32)

    R = np.array([[np.cos(theta_rad), -np.sin(theta_rad), 0],
                  [np.sin(theta_rad),  np.cos(theta_rad), 0],
                  [0, 0, 1]], dtype=np.float32)

    S = np.array([[scale, 0, 0],
                  [0, scale, 0],
                  [0, 0, 1]], dtype=np.float32)

    P = np.array([[1, 0, 0],
                  [0, 1, 0],
                  [persp_x, persp_y, 1]], dtype=np.float32)

    # Homographie complète : T * R * S * P
    H = T @ R @ S @ P
    return H

H = build_homography_matrix(tx, ty, theta, scale, persp_x, persp_y)

# Filtrer les fichiers image valides
valid_ext = [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]
image_paths = [p for p in Path(input_folder).iterdir() if p.suffix.lower() in valid_ext]

# Appliquer à chaque image
for img_path in image_paths:
    img = cv2.imread(str(img_path))
    if img is None:
        print(f"Warning: Skipping unreadable image {img_path.name}")
        continue

    warped = cv2.warpPerspective(img, H, (width, height))
    output_path = Path(output_folder) / img_path.name
    cv2.imwrite(str(output_path), warped)
    print(f"Saved transformed image to {output_path}")

print("✅ All images processed.")
