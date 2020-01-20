from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from scrollImg import ScrollableImage
import os


directory = "images"


def exitConfirm():
    MsgBox = messagebox.askquestion(
        'Exit Application', 'Are you sure you want to exit the application', icon='warning')
    if MsgBox == 'yes':
        exit()

def nextPage():
    print("next page")
    ## TODO


def labelImage(imgPath):
    root = Tk()
    img_frame = Frame(root)
    control_frame = Frame(root)
    output_frame = Frame(root)

    pilImage = Image.open(imgPath)
    tkImage = ImageTk.PhotoImage(pilImage, master=root)
    img = ScrollableImage(img_frame, image=tkImage,
                          width=pilImage.width, height=pilImage.height).pack()

    nextButton = Button(control_frame, text="Next Page",
                        command=nextPage).pack(side=TOP)
    exitButton = Button(control_frame, text="Exit",
                        command=exitConfirm).pack(side=BOTTOM)

    output_frame.pack(side=LEFT)
    img_frame.pack(side=LEFT)
    control_frame.pack(side=RIGHT)

    root.mainloop()


for filename in os.listdir(directory):
    if filename.endswith(".tif"):
        print("Labelling " + str(filename) + "...")

        path = os.path.join(directory, filename)

        labelImage(path)
