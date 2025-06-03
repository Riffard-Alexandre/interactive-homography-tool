# 🔧 Interactive Homography Tuning Tool

This Python tool provides an **interactive interface** to manually fine-tune a **homography transformation** between two images (e.g., a **Visible** image and a **SWIR** image). It helps align the two images visually by allowing real-time manual adjustments.

## 🖼️ Use Cases

- Align a visible-spectrum image with a SWIR image taken from a different angle.
- Instantly visualize the effects of translation, rotation, zoom, and perspective warp.
- Manually find the optimal transformation before using automated tools.

---

## ⚙️ Features

- Loads two images (`swir.png` and `visible.png`)
- Transparent overlay of the visible image on the reference
- Manual control of:
  - Translation (X/Y)
  - Rotation
  - Zoom / Scale
  - Perspective distortion (horizontal / vertical)
- Real-time parameter display
- Console output of current parameters on demand

---

## 🎮 Keyboard Controls

| Key | Action |
|-----|--------|
| `W/S` | Move Up / Down |
| `A/D` | Move Left / Right |
| `Q/E` | Rotate |
| `Z/X` | Zoom In / Out |
| `I/K` | Vertical Perspective Warp |
| `J/L` | Horizontal Perspective Warp |
| `+/-` | Adjust overlay transparency |
| `P` | Print current parameters |
| `ESC` | Exit the program |

---

## 🛠️ Installation

### 1. Requirements

Install dependencies with:

```bash
pip install numpy opencv-python
```

### 2. Prepare Your Images
Put your two aligned images in the same directory as the script:
- ```swir.png``` — Reference image (background)
- ```visible.png``` — Image to warp (forground)
Both images should have the same resolution (or be pre-resized).

## 🚀 Running the Tool
```bash
python homography_interface.py
```
A window will open showing the overlay in real time as you adjust it.

## 📝 Example Output
When you press ```P```, you’ll get output like this:
```makefile
--- Current Parameters ---
tx: 12.0
ty: -5.0
theta: 3.0
scale: 1.1
persp_x: 0.002
persp_y: -0.001
alpha: 0.5
--------------------------
```
These values can be used to compute or apply a ```cv2.warpPerspective()``` transformation later.

## 💡 Potential Improvements
- Add sliders (OpenCV trackbars) for visual adjustment
- Save current parameters to a ```.json``` file
- Add a "Reset" button
- Export the full homography matrix

## 🧪 Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License
This project is licensed under the MIT License – see the LICENSE file for details.

## ✨ Acknowledgements
Designed to simplify image alignment and easily visualise the result. 🚀
Good luck in your project. 😺