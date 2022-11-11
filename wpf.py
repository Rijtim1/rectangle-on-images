from tkinter import *
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

class Display(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)

        # set the window name
        self.master.title('Rectangle on Image')
        
        self.pack()
        self.makeWidgets()
        self.size = None
        self.shapes = []
        self.canDraw = False
        self.color = "red" # default color

    def makeWidgets(self):
        # navigation bar
        nav = Frame(self)
        Button(nav, text='Load Image', command=self.onOpen).pack(side=LEFT)
        Button(nav, text='Draw', command=self.letDraw).pack(side=LEFT)
        Button(nav, text='Pick Color', command=self.pickColor).pack(side=LEFT)
        Button(nav, text='Save', command=self.saveFile).pack(side=LEFT)
        Button(nav, text='Quit', command=self.quit).pack(side=LEFT)
        nav.pack(side=TOP, fill=X)

        self.data = Canvas(self, width=500, height=500, bg='white')
        self.data.pack(expand=YES, fill=BOTH)

    def pickColor(self):
        color = colorchooser.askcolor()
        self.color = color[1]
        print(self.color)
    
    def saveFile(self):
        print("Save File")
        pass

    def quit(self) -> None:
        return super().quit()

    def onOpen(self):
        filename = askopenfilename()
        if filename:
            # load the image file
            img = Image.open(filename)
            self.size = img.size
            x1, y1 = self.size
            # resize the canvas to image size
            self.data.config(width=img.width, height=img.height)
            # create a photo image object
            img = ImageTk.PhotoImage(img)
            # display the image
            self.data.create_image(0, 0, image=img, anchor=NW)
            rec = self.data.create_rectangle(0,0, x1, y1)
            self.data.image = img

    def letDraw(self):
        shape = []

        def draw_shape(shape):
            rec = self.data.create_rectangle(*shape, activeoutline="red", outline=self.color)
            self.shapes.append(rec)

        def click(event):
            print(f"clicked at {event.x} {event.y}")
            shape.append(event.x)
            shape.append(event.y)
        
        def release(event):
            x1, y1 = self.size
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
            draw_shape(shape)
            print(f"clicked at {event.x} {event.y}")

        self.data.bind('<ButtonPress-1>', click)
        self.data.bind('<ButtonRelease-1>', release)


if __name__ == '__main__':
    Display().mainloop()

            