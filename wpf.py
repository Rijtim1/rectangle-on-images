from tkinter import *
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk


class Display(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)

        # set the window name
        self.master.title('Rectangle on Image')
        self.imageLoaded = False
        self.pack()
        self.makeWidgets()
        self.size = None
        self.shapes = []
        self.color = "red"  # default color
        self.filename = None

    def makeWidgets(self):
        # navigation bar
        nav = Frame(self)
        load = Button(nav, text='Load Image',
                      command=self.onOpen).pack(side=LEFT)
        draw = Button(nav, text='Draw', command=self.letDraw).pack(side=LEFT)
        pickColor = Button(nav, text='Pick Color',
                           command=self.pickColor).pack(side=LEFT)
        # save = Button(nav, text='Save', command=self.saveFile).pack(side=LEFT)
        help = Button(nav, text='Help', command=self.help).pack(side=LEFT)
        quit = Button(nav, text='Quit', command=self.quit).pack(side=LEFT)        
        nav.pack(side=TOP, fill=X)

        self.data = Canvas(self, width=500, height=500, bg='white')
        self.data.pack(expand=YES, fill=BOTH)

    def pickColor(self):
        color = colorchooser.askcolor()
        self.color = color[1]
        # print(self.color)

    def help(self):
        showinfo("Help", "1. Load an image first\n2. Select Draw\n3. Select a color\n4. Click and drag to draw a rectangle\n5. Repeat steps 2-4 to draw more rectangles\n6. Select Quit to exit the program")

    # def saveFile(self):
    #     # error handling for when the user tires to save without loading an image first
    #     try:
    #         x1, y1 = self.size
    #         x2, y2 = self.size
    #         self.shapes.append(self.data.create_rectangle(
    #             x1, y1, x2, y2, fill=self.color))
    #         self.data.update()
    #         self.data.postscript(file=self.filename + ".ps", colormode='color')
    #         showinfo("Success", "File saved successfully")
    #     except:
    #         showinfo("Error", "Please load an image first!")
    #         return

    def quit(self) -> None:
        return super().quit()

    def onOpen(self):
        filename = askopenfilename()
        if filename:
            # load the image file
            # error handling for when something happens when trying to load the image
            try:
                img = Image.open(filename)
                name = filename.split("/")[-1]
                self.filename = name

            except:
                showinfo(title='Open Image File',
                         message='Failed to load {}'.format(filename))
                return

            self.size = img.size
            x1, y1 = self.size
            # resize the canvas to image size
            self.data.config(width=img.width, height=img.height)
            # create a photo image object
            img = ImageTk.PhotoImage(img)
            # display the image
            self.data.create_image(0, 0, image=img, anchor=NW)
            rec = self.data.create_rectangle(0, 0, x1, y1)
            self.data.image = img
        self.imageLoaded = True

    def letDraw(self):

        shape = []

        def draw_shape(shape):
            rec = self.data.create_rectangle(
                *shape, activeoutline="red", outline=self.color)
            self.shapes.append(rec)

        def click(event):
            # print(f"clicked at {event.x} {event.y}")
            shape.append(event.x)
            shape.append(event.y)

        def release(event):
            # error handling for when the user tires to draw without loading an image first
            try:
                x1, y1 = self.size
            except:
                showinfo("Error", "Please load an image first!")
                return

            if event.x > x1:
                event.x = x1
            if event.x < 0:
                event.x = 0
            if event.y > y1:
                event.y = y1
            if event.y < 0:
                event.y = 0
            shape.append(event.x)
            shape.append(event.y)
            # error handling for when user tries to draw on the image without selecting draw first
            try:
                draw_shape(shape)
            except:
                showinfo("Error", "Please select Draw First!")
                return
            # print(f"clicked at {event.x} {event.y}")

        self.data.bind('<ButtonPress-1>', click)
        self.data.bind('<ButtonRelease-1>', release)


if __name__ == '__main__':
    Display().mainloop()
