from typing import Literal
from abc import ABC, abstractmethod
import tkinter as tk

Shapes = Literal["Dot", "Line", "Rectangle", "Ellipse"]


class EditorCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        self.shapes = []
        self._shape_strategy: _ShapeStrategy = None

        # Bind mouse events
        self.bind("<ButtonPress-1>", self.on_mouse_down)
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease-1>", self.on_mouse_up)

    def select_shape(self, strategy_name: Shapes):
        self._shape_strategy = _SHAPE_STRATEGIES[strategy_name]()

    def on_mouse_down(self, event):
        if not self._shape_strategy:
            return
        self._shape_strategy.start_drawing(self, event)

    def on_mouse_drag(self, event):
        if not self._shape_strategy:
            return
        self._shape_strategy.draw(self, event)

    def on_mouse_up(self, event):
        if not self._shape_strategy:
            return
        self._shape_strategy.stop_drawing(self, event)

    def clear_canvas(self):
        self.delete("all")
        self.shapes.clear()


class _ShapeStrategy(ABC):
    def __init__(self):
        super().__init__()

        self.shape_id = None
        self.start_x = None
        self.start_y = None

    @abstractmethod
    def start_drawing(self, canvas: EditorCanvas, event: tk.Event):
        canvas.shapes.append(self.shape_id)

    @abstractmethod
    def draw(self, canvas: EditorCanvas, event: tk.Event):
        pass

    @abstractmethod
    def stop_drawing(self, canvas: EditorCanvas, event: tk.Event):
        pass


class _DotStrategy(_ShapeStrategy):
    def start_drawing(self, canvas: EditorCanvas, event: tk.Event):
        self.shape_id = canvas.create_oval(
            event.x - 1, event.y - 1,
            event.x + 1, event.y + 1,
            fill="black"
        )

        super().start_drawing(canvas, event)

        return self.shape_id

    def draw(self, canvas: EditorCanvas, event):
        pass

    def stop_drawing(self, canvas: EditorCanvas, event):
        pass


class _LineStrategy(_ShapeStrategy):
    def start_drawing(self, canvas: EditorCanvas, event: tk.Event):
        self.start_x, self.start_y = event.x, event.y

        self.shape_id = canvas.create_line(
            self.start_x, self.start_y,
            event.x, event.y
        )

        super().start_drawing(canvas, event)

    def draw(self, canvas: EditorCanvas, event: tk.Event):
        canvas.coords(
            self.shape_id, self.start_x, self.start_y,
            event.x, event.y
        )

    def stop_drawing(self, canvas: EditorCanvas, event: tk.Event):
        pass


class _RectangleStrategy(_ShapeStrategy):
    def start_drawing(self, canvas: EditorCanvas, event: tk.Event):
        self.start_x, self.start_y = event.x, event.y
        self.shape_id = canvas.create_rectangle(
            self.start_x, self.start_y,
            event.x, event.y
        )

        super().start_drawing(canvas, event)

    def draw(self, canvas: EditorCanvas, event: tk.Event):
        canvas.coords(
            self.shape_id, self.start_x, self.start_y,
            event.x, event.y
        )

    def stop_drawing(self, canvas: EditorCanvas, event: tk.Event):
        pass


class _EllipseStrategy(_ShapeStrategy):
    def start_drawing(self, canvas: EditorCanvas, event: tk.Event):
        self.start_x, self.start_y = event.x, event.y
        self.shape_id = canvas.create_oval(
            self.start_x, self.start_y,
            event.x, event.y
        )

        super().start_drawing(canvas, event)

    def draw(self, canvas: EditorCanvas, event: tk.Event):
        canvas.coords(
            self.shape_id, self.start_x, self.start_y,
            event.x, event.y
        )

    def stop_drawing(self, canvas: EditorCanvas, event: tk.Event):
        pass


_SHAPE_STRATEGIES = {
    "Dot": _DotStrategy,
    "Line": _LineStrategy,
    "Rectangle": _RectangleStrategy,
    "Ellipse": _EllipseStrategy,
}
