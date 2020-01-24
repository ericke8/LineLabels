import tkinter
from PIL import ImageTk, Image
import platform

OS = platform.system()


class ScrollableImage(tkinter.Canvas):
    def __init__(self, parent, master=None, **kw):
        self.parent = parent
        self.image = kw.pop('image', None)
        super(ScrollableImage, self).__init__(master=master, **kw)

        self.width = self.image.width()
        self.height = self.image.height()

        #self['highlightthickness'] = 0
        self.propagate(0)  # wont let the scrollbars rule the size of Canvas
        self.create_image(0, 0, anchor='ne', image=self.image)

        # Vertical scrollbar
        self.v_scroll = tkinter.Scrollbar(self, orient='vertical', width=6)
        self.v_scroll.pack(side='right', fill='y')

        # Set the scrollbars to the canvas
        self.config(yscrollcommand=self.v_scroll.set)

        # Set canvas view to the scrollbars
        self.v_scroll.config(command=self.yview)

        # Assign the region to be scrolled
        self.config(scrollregion=self.bbox('all'))

        self.focus_set()

        if OS == "Linux":
            self.bind_class(self, '<Button-4>', self.mouse_scroll)
            self.bind_class(self, '<Button-5>', self.mouse_scroll)
        else:
            self.bind_class(self, "<MouseWheel>", self.mouse_scroll)

        self.bind_class(self, "<Button-1>", self.mouse_click)

    def mouse_scroll(self, evt):
        if OS == "Windows":
            self.yview_scroll(int(-1*(evt.delta/120)), 'units')  # For windows
        elif OS == "Darwin":
            self.yview_scroll(-1*(evt.delta), 'units')  # For MacOS
        elif OS == "Linux":
            if evt.num == 4:
                self.yview_scroll(-1, 'units')
            elif evt.num == 5:
                self.yview_scroll(1, 'units')

    def mouse_click(self, evt):
        y = self.canvasy(evt.y)
        if y > self.height:
            y = self.height
        if y < 0:
            y = 0

        if self.parent.labelMode.get() == True:
            if y not in self.parent.lineCuts:
                lineId = self.create_line(0, y, -1 * self.width, y, fill='red', width=3)
                self.parent.lineCuts[y] = lineId
        else:
            for line in self.parent.lineCuts.keys():
                if line < y + 5 and line > y - 5:
                    self.delete(self.parent.lineCuts[line])
                    del self.parent.lineCuts[line]
                    break
