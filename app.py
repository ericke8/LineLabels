import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import sys

from scrollImg import ScrollableImage


class LineLabel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.imgPath = kwargs.pop('imgPath', None)
        self.outputDir = kwargs.pop('outputDir', None)
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.control_window = tk.Toplevel(self.parent)  
        self.labelMode = tk.BooleanVar(value=True)
        self.lineCuts = {}
        
        if not self.outputDir:
            self.outputDir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(self.imgPath))), "lineCuts")
            if not os.path.exists(self.outputDir):
                os.makedirs(self.outputDir)

        self.setupUI()

    def setupUI(self):
        self.parent.title("LineLabel")
        self.img_frame = tk.Frame(self)
        self.control_frame = tk.Frame(self.control_window)
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
        outputFile = os.path.basename(self.imgPath).replace('.tif', '_cutLines.csv')
        fout = open(os.path.join(self.outputDir, outputFile), "w")
        for line in cutIndices:
            fout.write(str(int(line)) + '\n')
        fout.close()


def labelImage(path, out):
    root = tk.Tk()
    LineLabel(root, imgPath=path, outputDir=out).pack(side="top", fill="both", expand=True)
    root.mainloop()

USAGE = "Usage: python app.py path_to_images_directory [optional path to output]"

if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Wrong number of args \n" + USAGE)
        exit()
    elif not os.path.isdir(sys.argv[1]) or not os.path.exists(sys.argv[1]):
        print("Invalid images directory \n" + USAGE)
        exit()
    else:
        directory = sys.argv[1]
        if len(sys.argv) == 3:
            if not os.path.exists(sys.argv[2]):
                print("Output directory does not exist \n" + USAGE)
                exit()
            elif not os.path.isdir(sys.argv[2]):
                print("Invalid output directory \n" + USAGE)
                exit()
            out = sys.argv[2]
        else:
            out = None
    
    for filename in os.listdir(directory):
        if filename.endswith(".tif"):
            print("Labelling " + str(filename) + "...")

            imgPath = os.path.join(directory, filename)

            labelImage(imgPath, out)
