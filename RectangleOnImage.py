from tkinter import *
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

class Display(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()

        self.image_loaded = False
        self.filename = None
        self.color = "red"  # default color
        self.shapes = []

        self.create_widgets()

    def create_widgets(self):
        # navigation bar
        nav = Frame(self)
        load_button = Button(nav, text='Load Image', command=self.on_open)
        load_button.pack(side=LEFT)
        draw_button = Button(nav, text='Draw', command=self.let_draw)
        draw_button.pack(side=LEFT)
        pick_color_button = Button(nav, text='Pick Color', command=self.pick_color)
        pick_color_button.pack(side=LEFT)
        help_button = Button(nav, text='Help', command=self.show_help)
        help_button.pack(side=LEFT)
        quit_button = Button(nav, text='Quit', command=self.quit)
        quit_button.pack(side=LEFT)        
        nav.pack(side=TOP, fill=X)

        self.canvas = Canvas(self, width=500, height=500, bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

    def pick_color(self):
        color = colorchooser.askcolor()
        self.color = color[1]

    def show_help(self):
        message = "1. Load an image first\n2. Select Draw\n3. Select a color\n4. Click and drag to draw a rectangle\n5. Repeat steps 2-4 to draw more rectangles\n6. Select Quit to exit the program"
        showinfo("Help", message)

    def on_open(self):
        filename = askopenfilename()
        if filename:
            # load the image file
            # error handling for when something happens when trying to load the image
            try:
                img = Image.open(filename)
                name = filename.split("/")[-1]
                self.filename = name
            except:
                showinfo(title='Open Image File', message='Failed to load {}'.format(filename))
                return

            self.size = img.size
            x1, y1 = self.size
            # resize the canvas to image size
            self.canvas.config(width=img.width, height=img.height)
            # create a photo image object
            img = ImageTk.PhotoImage(img)
            # display the image
            self.canvas.create_image(0, 0, image=img, anchor=NW)
            rec = self.canvas.create_rectangle(0, 0, x1, y1)
            self.data.image = img
        self.imageLoaded = True

    def let_draw(self):
        self.shape = []
        self.canvas.bind('<ButtonPress-1>', self.on_click)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)

    def on_click(self, event):
        self.shape.append(event.x)
        self.shape.append(event.y)

    def on_release(self, event):
        try:
            x1, y1 = self.size
        except AttributeError:
            showinfo("Error", "Please load an image first!")
            return

        event.x = min(max(event.x, 0), x1)
        event.y = min(max(event.y, 0), y1)
        self.shape.append(event.x)
        self.shape.append(event.y)

        rec = self.canvas.create_rectangle(*self.shape, activeoutline="red", outline=self.color)
        self.shapes.append(rec)



if __name__ == '__main__':
    Display().mainloop()
