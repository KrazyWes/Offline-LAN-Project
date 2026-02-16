# app/ui/components/toggle_switch.py
"""
iOS-style toggle switch component matching Figma specifications.
From COMPLETE_SYSTEM_ALGORITHM.md section 4.2.2
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, Property, Signal
from PySide6.QtGui import QPainter, QColor, QPen
from app.ui.components.styles import COLORS, DIMENSIONS

class ToggleSwitch(QWidget):
    """iOS-style toggle switch with smooth animation"""
    
    toggled = Signal(bool)
    
    def __init__(self, parent=None, checked=False):
        super().__init__(parent)
        self._checked = checked
        self._circle_position = 24 if checked else 4
        
        self.setFixedSize(44, 24)  # w-11, h-6
        self.setCursor(Qt.PointingHandCursor)
        
        # Animation
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.setDuration(300)
    
    @Property(int)
    def circle_position(self):
        return self._circle_position
    
    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle()
    
    def toggle(self):
        """Toggle the switch state"""
        self._checked = not self._checked
        
        # Animate circle
        self.animation.setStartValue(self._circle_position)
        self.animation.setEndValue(24 if self._checked else 4)
        self.animation.start()
        
        self.toggled.emit(self._checked)
    
    def setChecked(self, checked: bool):
        """Set checked state without animation"""
        if self._checked != checked:
            self._checked = checked
            self._circle_position = 24 if checked else 4
            self.update()
            self.toggled.emit(self._checked)
    
    def isChecked(self) -> bool:
        return self._checked
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background track
        if self._checked:
            painter.setBrush(QColor(COLORS['blue_600']))
        else:
            painter.setBrush(QColor(COLORS['gray_300']))
        
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, 44, 24, 12, 12)
        
        # Draw circle (slider)
        painter.setBrush(QColor(COLORS['white']))
        painter.drawEllipse(self._circle_position, 4, 16, 16)
