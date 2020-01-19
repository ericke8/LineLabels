import tkinter
from PIL import ImageTk, Image
import platform

OS = platform.system()


class ScrollableImage(tkinter.Canvas):
    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        super(ScrollableImage, self).__init__(master=master, **kw)

        self['highlightthickness'] = 0
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
