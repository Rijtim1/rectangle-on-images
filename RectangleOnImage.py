from tkinter import *
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

class Rectangle:
    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.selected = False

class RectangleDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rectangle Drawing App")
        self.canvas_width = 800
        self.canvas_height = 600
        self.rectangles = []
        self.selected_rectangle = None
        self.color = "red"
        self.start_x = None
        self.start_y = None

        self.create_widgets()

    def create_widgets(self):
        # Load Image button
        load_button = Button(self.root, text="Load Image", command=self.load_image)
        load_button.pack()

        # Canvas for drawing
        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        # Color Palette button
        color_button = Button(self.root, text="Pick Color", command=self.pick_color)
        color_button.pack()

    def load_image(self):
        filename = askopenfilename()
        if filename:
            try:
                img = Image.open(filename)
                self.image = ImageTk.PhotoImage(img)
                self.canvas.config(width=self.image.width(), height=self.image.height())
                self.canvas.create_image(0, 0, image=self.image, anchor=NW)
            except Exception as e:
                print("Failed to load image:", str(e))

    def pick_color(self):
        color = colorchooser.askcolor()
        self.color = color[1]

    def on_canvas_click(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_canvas_drag(self, event):
        if self.start_x is not None and self.start_y is not None:
            self.canvas.delete("temp_rectangle")  # Remove previous temporary rectangle
            x = min(event.x, self.start_x)
            y = min(event.y, self.start_y)
            width = abs(event.x - self.start_x)
            height = abs(event.y - self.start_y)
            self.draw_rectangle(x, y, width, height, self.color, tag="temp_rectangle")

    def on_canvas_release(self, event):
        if self.start_x is not None and self.start_y is not None:
            self.canvas.delete("temp_rectangle")  # Remove temporary rectangle
            x = min(event.x, self.start_x)
            y = min(event.y, self.start_y)
            width = abs(event.x - self.start_x)
            height = abs(event.y - self.start_y)
            self.draw_rectangle(x, y, width, height, self.color)
            self.start_x = None
            self.start_y = None

    def draw_rectangle(self, x, y, width, height, color, tag=None):
        rectangle = Rectangle(x, y, x + width, y + height, color)
        self.rectangles.append(rectangle)
        self.canvas.create_rectangle(rectangle.x1, rectangle.y1, rectangle.x2, rectangle.y2, outline=color, tag=tag)

    def mainloop(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = RectangleDrawingApp(root)
    app.mainloop()
