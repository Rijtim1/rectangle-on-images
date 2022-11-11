from tkinter import *
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

    def makeWidgets(self):
        self.b1 = Button(self, text='File Open', command=self.onOpen).pack()
        self.b2 = Button(self, text='Draw Shapes', command=self.letDraw).pack()
        # self.b3 = Button(self, text='Exit Draw', command=self.exitDraw).pack()
        # initialize the canvas
        # size of canvas will be the size of the image
        self.data = Canvas(self, width=500, height=500, bg='white')
        self.data.pack(expand=YES, fill=BOTH)

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
            rec = self.data.create_rectangle(*shape, activeoutline="red", outline="yellow")
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

            