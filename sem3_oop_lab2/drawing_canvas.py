import tkinter as tk
from typing import Literal
from .shape_strategies import SHAPE_STRATEGIES, ShapeStrategy

Shapes = Literal["Dot", "Line", "Rectangle", "Ellipse"]


class DrawingCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        self.current_strategy: ShapeStrategy = None

        # Bind mouse events
        self.bind("<ButtonPress-1>", self.on_mouse_down)
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease-1>", self.on_mouse_up)

    def select_shape(self, strategy_name: Shapes):
        self.current_strategy = SHAPE_STRATEGIES[strategy_name]()

    def on_mouse_down(self, event):
        if not self.current_strategy:
            return
        self.current_strategy.start_drawing(self, event)

    def on_mouse_drag(self, event):
        if not self.current_strategy:
            return
        self.current_strategy.draw(self, event)

    def on_mouse_up(self, event):
        if not self.current_strategy:
            return
        self.current_strategy.stop_drawing(self, event)

    def clear_canvas(self):
        self.delete("all")
