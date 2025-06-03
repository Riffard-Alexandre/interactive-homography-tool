import cv2
import numpy as np

# === PARAMÈTRES INITIAUX ===
params = {
    'tx': 0.0,  # translation x
    'ty': 0.0,  # translation y
    'theta': 0.0,  # rotation en degrés
    'scale': 1.0,  # zoom
    'persp_x': 0.0,  # perspective horizontale
    'persp_y': 0.0,  # perspective verticale
    'alpha': 0.5  # transparence image visible
}

step = 1.0  # pas de modification
scale_step = 0.05
angle_step = 1.0
persp_step = 0.001

# === CHARGEMENT DES IMAGES ===
swir = cv2.imread(r"C:\Users\Riffard\Documents\Datasets\Cerema_05-06_05_2025\5\03-calib_swir\seq_00709_1746512979_698878153.tiff")
visible = cv2.imread(r"C:\Users\Riffard\Documents\Datasets\Cerema_05-06_05_2025\5\03-calib_vis\seq_00710_1746512979_701329716.tiff")

if swir is None or visible is None:
    raise ValueError("Images non trouvées ! Assurez-vous que l'image SWIR et/ou l'image Visible existent.")

height, width = swir.shape[:2]

# === CRÉATION DE LA FENÊTRE ===
cv2.namedWindow("Ajustement Homographique")

# === FONCTION POUR CONSTRUIRE LA MATRICE D'HOMOGRAPHIE ===
def get_homography(params):
    tx, ty = params['tx'], params['ty']
    theta = np.deg2rad(params['theta'])
    scale = params['scale']
    px, py = params['persp_x'], params['persp_y']

    # Matrices de transformation
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0, 1]], dtype=np.float32)

    R = np.array([[np.cos(theta), -np.sin(theta), 0],
                  [np.sin(theta),  np.cos(theta), 0],
                  [0, 0, 1]], dtype=np.float32)

    S = np.array([[scale, 0, 0],
                  [0, scale, 0],
                  [0, 0, 1]], dtype=np.float32)

    P = np.array([[1, 0, 0],
                  [0, 1, 0],
                  [px, py, 1]], dtype=np.float32)

    H = T @ R @ S @ P
    return H

# === BOUCLE PRINCIPALE ===
while True:
    # Calcul de l’homographie et transformation de l’image visible
    H = get_homography(params)
    warped_visible = cv2.warpPerspective(visible, H, (width, height))

    # Fusion des deux images
    blended = cv2.addWeighted(warped_visible, params['alpha'], swir, 1 - params['alpha'], 0)

    # Affichage des paramètres
    param_text = f"Tx:{params['tx']} Ty:{params['ty']} Rot:{params['theta']}° Scale:{params['scale']:.2f} Px:{params['persp_x']:.4f} Py:{params['persp_y']:.4f}"
    cv2.putText(blended, param_text, (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 1)

    cv2.imshow("Ajustement Homographique", blended)

    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC pour quitter
        break
    elif key == ord('w'):
        params['ty'] -= step
    elif key == ord('s'):
        params['ty'] += step
    elif key == ord('a'):
        params['tx'] -= step
    elif key == ord('d'):
        params['tx'] += step
    elif key == ord('q'):
        params['theta'] -= angle_step
    elif key == ord('e'):
        params['theta'] += angle_step
    elif key == ord('z'):
        params['scale'] += scale_step
    elif key == ord('x'):
        params['scale'] -= scale_step
    elif key == ord('j'):
        params['persp_x'] -= persp_step
    elif key == ord('l'):
        params['persp_x'] += persp_step
    elif key == ord('i'):
        params['persp_y'] -= persp_step
    elif key == ord('k'):
        params['persp_y'] += persp_step
    elif key == ord('+') or key == ord('='):
        params['alpha'] = min(params['alpha'] + 0.05, 1.0)
    elif key == ord('-') or key == ord('_'):
        params['alpha'] = max(params['alpha'] - 0.05, 0.0)
    elif key == ord('p'):
        print("\n--- Paramètres actuels ---")
        for k, v in params.items():
            print(f"{k}: {v}")
        print("--------------------------")

cv2.destroyAllWindows()
