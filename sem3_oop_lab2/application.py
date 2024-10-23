import tkinter as tk

from .editor_canvas import EditorCanvas, Shapes


class Application(tk.Tk):
    def __init__(self, screenName=None, baseName=None,
                 className="oop_lab2", useTk=True, sync=False,
                 use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.resizable(False, False)
        self.geometry("500x500")

        self._editor_canvas = EditorCanvas(self)
        self._menubar = _MenuBar(self)

        # Application config
        self.config(menu=self._menubar, border=5)

        # Placing widgets
        self._editor_canvas.pack(fill=tk.BOTH, expand=True)
        # self.menubar.grid(row=0, column=0)

    def select_shape(self, shape: Shapes):
        self._editor_canvas.select_shape(shape)

    def clear_canvas(self):
        self._editor_canvas.clear_canvas()


class _MenuBar(tk.Menu):
    def __init__(self, parent: Application):
        super().__init__(parent)

        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(
            label="Очистити",
            command=parent.clear_canvas
        )

        object_menu = tk.Menu(self, tearoff=0)
        object_menu.add_radiobutton(
            label="Крапка",
            command=(lambda: parent.select_shape("Dot"))
        )
        object_menu.add_radiobutton(
            label="Лінія",
            command=(lambda: parent.select_shape("Line"))
        )
        object_menu.add_radiobutton(
            label="Прямокутник",
            command=(lambda: parent.select_shape("Rectangle"))
        )
        object_menu.add_radiobutton(
            label="Еліпс",
            command=(lambda: parent.select_shape("Ellipse"))
        )

        info_menu = tk.Menu(self, tearoff=0)

        self.add_cascade(label="Файл", menu=file_menu)
        self.add_cascade(label="Об’єкти", menu=object_menu)
        self.add_cascade(label="Довідка", menu=info_menu)
