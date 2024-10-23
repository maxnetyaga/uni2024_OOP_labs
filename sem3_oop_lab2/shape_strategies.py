from abc import ABC, abstractmethod
import tkinter as tk


class ShapeStrategy(ABC):
    def __init__(self):
        super().__init__()

        self.shape_id = None
        self.start_x = None
        self.start_y = None

    @abstractmethod
    def start_drawing(self, canvas: tk.Canvas, event: tk.Event) -> int:
        pass

    @abstractmethod
    def draw(self, canvas: tk.Canvas, event: tk.Event):
        pass

    @abstractmethod
    def stop_drawing(self, canvas: tk.Canvas, event: tk.Event):
        pass


class DotStrategy(ShapeStrategy):
    def start_drawing(self, canvas: tk.Canvas, event: tk.Event) -> int:
        self.shape_id = canvas.create_oval(
            event.x - 1, event.y - 1,
            event.x + 1, event.y + 1,
            fill="black"
        )

        return self.shape_id

    def draw(self, canvas: tk.Canvas, event):
        pass

    def stop_drawing(self, canvas: tk.Canvas, event):
        pass


class LineStrategy(ShapeStrategy):
    def start_drawing(self, canvas: tk.Canvas, event: tk.Event) -> int:
        self.start_x, self.start_y = event.x, event.y

        self.shape_id = canvas.create_line(
            self.start_x, self.start_y,
            event.x, event.y
        )

        return self.shape_id

    def draw(self, canvas: tk.Canvas, event: tk.Event):
        canvas.coords(
            self.shape_id, self.start_x, self.start_y,
            event.x, event.y
        )

    def stop_drawing(self, canvas: tk.Canvas, event: tk.Event):
        pass


class RectangleStrategy(ShapeStrategy):
    def start_drawing(self, canvas: tk.Canvas, event: tk.Event) -> int:
        self.start_x, self.start_y = event.x, event.y
        self.shape_id = canvas.create_rectangle(
            self.start_x, self.start_y,
            event.x, event.y
        )
        return self.shape_id

    def draw(self, canvas: tk.Canvas, event: tk.Event):
        canvas.coords(
            self.shape_id, self.start_x, self.start_y,
            event.x, event.y
        )

    def stop_drawing(self, canvas: tk.Canvas, event: tk.Event):
        pass


class EllipseStrategy(ShapeStrategy):
    def start_drawing(self, canvas: tk.Canvas, event: tk.Event):
        self.start_x, self.start_y = event.x, event.y
        self.shape_id = canvas.create_oval(
            self.start_x, self.start_y,
            event.x, event.y
        )

    def draw(self, canvas: tk.Canvas, event: tk.Event):
        canvas.coords(
            self.shape_id, self.start_x, self.start_y,
            event.x, event.y
        )

    def stop_drawing(self, canvas: tk.Canvas, event: tk.Event):
        pass


SHAPE_STRATEGIES = {
    "Dot": DotStrategy,
    "Line": LineStrategy,
    "Rectangle": RectangleStrategy,
    "Ellipse": EllipseStrategy,
}
