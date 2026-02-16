# app/ui/components/icon_utils.py
"""
Icon utility functions with fallback handling for missing icons.
"""
from __future__ import annotations
import os
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtCore import QSize, Qt

def asset_path(*parts: str) -> str:
    """Get absolute path to asset file"""
    # Works if you run from project root
    return os.path.join("app", "assets", *parts)

def icon(rel_path: str) -> QIcon:
    """
    Load icon from path, with fallback to empty icon if not found.
    rel_path example: "icons/sidebar/cashier_overview.png"
    """
    path = asset_path(*rel_path.split("/"))
    if os.path.exists(path):
        return QIcon(path)
    else:
        # Return empty icon as fallback (prevents crashes)
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        return QIcon(pixmap)

def set_icon(btn, rel_path: str, size: int = 18):
    """Set icon on button with size"""
    btn.setIcon(icon(rel_path))
    btn.setIconSize(QSize(size, size))
