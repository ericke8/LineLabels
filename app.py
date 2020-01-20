import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import sys
import csv

from scrollImg import ScrollableImage


class LineLabel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.imgPath = kwargs.pop('imgPath', None)

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.labelMode = tk.BooleanVar(value=True)
        self.lineCuts = {}
        self.setupUI()

    def setupUI(self):
        self.parent.title("LineLabel")
        self.img_frame = tk.Frame(self)
        self.control_frame = tk.Frame(self)
        self.switch_frame = tk.Frame(self.control_frame)
        #output_frame = Frame(root)

        pilImage = Image.open(self.imgPath)
        tkImage = ImageTk.PhotoImage(pilImage, master=self.img_frame)
        self.img = ScrollableImage(self, self.img_frame, image=tkImage,
                                   width=pilImage.width, height=pilImage.height).pack()

        self.addButton = tk.Radiobutton(self.switch_frame, text="Add", variable=self.labelMode,
                                        indicatoron=False, value=True, width=8).pack(side=tk.TOP)
        self.removeButton = tk.Radiobutton(self.switch_frame, text="Remove", variable=self.labelMode,
                                           indicatoron=False, value=False, width=8).pack(side=tk.TOP)

        self.exitButton = tk.Button(self.control_frame, text="Exit App",
                                    command=self.exitConfirm).pack(side=tk.BOTTOM)
        self.nextButton = tk.Button(self.control_frame, text="Next Page",
                                    command=self.nextPage).pack(side=tk.BOTTOM)

        self.switch_frame.pack(side=tk.TOP)

        self.img_frame.pack(side=tk.LEFT)
        # self.output_frame.pack(side=tk.RIGHT)
        self.control_frame.pack(side=tk.RIGHT)

    def exitConfirm(self):
        MsgBox = messagebox.askquestion(
            'Exit Application', 'Are you sure you want to exit the application?', icon='warning')
        if MsgBox == 'yes':
            exit()

    def nextPage(self):
        MsgBox = messagebox.askquestion(
            'Next Page', 'Are you sure you are done with this page?', icon='warning')
        if MsgBox == 'yes':
            self.writeCutInfo()
            self.parent.destroy()

    def writeCutInfo(self):
        cutIndices = list(self.lineCuts)
        cutIndices.sort()
        outputFile = self.imgPath.replace('.tif', '_cutLines.csv')
        fout = open(outputFile, "w")
        for line in cutIndices:
            fout.write(str(int(line)) + '\n')
        fout.close()


def labelImage(path):
    root = tk.Tk()
    LineLabel(root, imgPath=path).pack(side="top", fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("Invalid Input \n Usage: python app.py [path to images directory]")
        exit()
    else:
        directory = sys.argv[1]
    
    for filename in os.listdir(directory):
        if filename.endswith(".tif"):
            print("Labelling " + str(filename) + "...")

            path = os.path.join(directory, filename)

            labelImage(path)
