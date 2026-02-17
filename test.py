# test.py - Display rooster_squad_1.png in a pop-up window (image box)
import os
from pathlib import Path

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QLabel
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

BG_PATH = Path(__file__).resolve().parent / "app" / "assets" / "backgrounds" / "rooster_squad_1.png"

if __name__ == "__main__":
    app = QApplication([])
    # Required on Windows: add plugins path so PySide6 can load PNG/JPG
    from PySide6 import QtCore
    app.addLibraryPath(os.path.join(os.path.dirname(QtCore.__file__), "plugins"))
    win = QWidget()
    win.setWindowTitle("Background Image Test")
    layout = QVBoxLayout(win)
    layout.setContentsMargins(0, 0, 0, 0)

    # Image box (QFrame container, same tactic as icon display)
    image_box = QFrame()
    image_box.setObjectName("imageBox")
    image_box.setStyleSheet("""
        QFrame#imageBox {
            background-color: #f0f0f0;
            border: 1px solid #ccc;
        }
    """)
    box_layout = QVBoxLayout(image_box)
    box_layout.setContentsMargins(0, 0, 0, 0)

    image_label = QLabel()
    image_label.setAlignment(Qt.AlignCenter)
    image_label.setScaledContents(True)
    if BG_PATH.exists():
        # Load from raw bytes (bypasses Qt file path handling)
        with open(BG_PATH, "rb") as f:
            data = f.read()
        img = QImage()
        img.loadFromData(data)
        if img.isNull():
            # Fallback: Pillow (file is AVIF - needs pillow-avif-plugin for .avif files)
            try:
                from PIL import Image
                import io
                # No format hint: auto-detect (supports AVIF if pillow-avif-plugin installed)
                pil_img = Image.open(io.BytesIO(data)).convert("RGBA")
                qimg = QImage(pil_img.tobytes(), pil_img.width, pil_img.height, QImage.Format.Format_RGBA8888)
                img = qimg
            except (ImportError, ValueError, OSError, RuntimeError):
                pass
        pix = QPixmap.fromImage(img) if not img.isNull() else QPixmap()
        if not pix.isNull():
            image_label.setPixmap(pix)
        else:
            image_label.setText(
                "Failed to load image.\n\nFile is AVIF format (not PNG).\n"
                "Convert to PNG, or: pip install pillow-avif-plugin"
            )
    else:
        image_label.setText(f"Image not found: {BG_PATH}")

    box_layout.addWidget(image_label)
    layout.addWidget(image_box)
    win.showMaximized()
    app.exec()
