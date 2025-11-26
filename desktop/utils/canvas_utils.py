"""
Utilitários para criar elementos visuais modernos com Canvas
Simula border-radius e box-shadow do CSS
"""
import tkinter as tk
from tkinter import Canvas

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=16, **kwargs):
    """
    Cria um retângulo arredondado no canvas
    """
    points = []
    # Canto superior esquerdo
    points.extend([x1 + radius, y1])
    points.extend([x2 - radius, y1])
    # Canto superior direito
    points.extend([x2, y1])
    points.extend([x2, y1 + radius])
    points.extend([x2, y2 - radius])
    # Canto inferior direito
    points.extend([x2, y2])
    points.extend([x2 - radius, y2])
    points.extend([x1 + radius, y2])
    # Canto inferior esquerdo
    points.extend([x1, y2])
    points.extend([x1, y2 - radius])
    points.extend([x1, y1 + radius])
    points.extend([x1, y1])
    
    return canvas.create_polygon(points, smooth=True, **kwargs)

def create_shadow_effect(parent, widget, shadow_color='rgba(0,0,0,0.1)', offset_x=0, offset_y=4, blur=8):
    """
    Cria um efeito de sombra usando um frame atrás do widget
    """
    shadow_frame = tk.Frame(
        parent,
        bg=shadow_color if isinstance(shadow_color, str) and not shadow_color.startswith('rgba') else '#E5E5E5'
    )
    return shadow_frame



