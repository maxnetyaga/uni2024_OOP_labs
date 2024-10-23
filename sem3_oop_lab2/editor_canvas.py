from typing import Literal
from abc import ABC, abstractmethod
import tkinter as tk

ShapeNames = Literal["Dot", "Line", "Rectangle", "Ellipse"]


class EditorCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        self._shape_to_draw: ShapeNames = None
        self._editable_shape: _Shape = None
        self._shapes = {}

        # Bind mouse events
        self.bind("<ButtonPress-1>", self.on_mouse_down)
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease-1>", self.on_mouse_up)

    def select_shape(self, shape_name: ShapeNames):
        self._shape_to_draw = shape_name

    def on_mouse_down(self, event):
        if not self._shape_to_draw:
            return

        self._editable_shape = _SHAPES[self._shape_to_draw]()
        self._editable_shape.start_drawing(self, event)

    def on_mouse_drag(self, event):
        if not self._shape_to_draw:
            return
        self._editable_shape.draw(self, event)

    def on_mouse_up(self, event):
        if not self._shape_to_draw:
            return
        self._editable_shape.stop_drawing(self, event)
        self._editable_shape = None

    def clear_canvas(self):
        self.delete("all")
        self._shapes.clear()


class _Shape(ABC):
    def __init__(self):
        super().__init__()

        self.shape_id = None
        self.start_x = None
        self.start_y = None

    @abstractmethod
    def start_drawing(self, canvas: EditorCanvas, event: tk.Event):
        canvas._shapes[self.shape_id] = self

    @abstractmethod
    def draw(self, canvas: EditorCanvas, event: tk.Event):
        pass

    @abstractmethod
    def stop_drawing(self, canvas: EditorCanvas, event: tk.Event):
        pass


class _Dot(_Shape):
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


class _Line(_Shape):
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


class _Rectangle(_Shape):
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


class _Ellipse(_Shape):
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


_SHAPES = {
    "Dot": _Dot,
    "Line": _Line,
    "Rectangle": _Rectangle,
    "Ellipse": _Ellipse,
}
