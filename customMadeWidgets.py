from Tkinter import *
from PIL import Image, ImageTk
from ttk import *
import Tkinter as tk
import tkFont

class dynamicOptionMenu(OptionMenu):
	# this little class is for a small option menu from which a dropdown selection box of both loaded
	# crystals and beams can be added to the current strategy - in the right window of the gui

	def __init__(self, *args, **kw):
		self._command = kw.get("command")
		OptionMenu.__init__(self, *args, **kw)
	def addOption(self, label):
		self["menu"].add_command(label=label,
		command=tk._setit(variable, label, self._command))

class VerticalScrolledFrame(Frame):
  	# this class is for a vertical scrolled frame that actually seems to work!

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=False)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # make a style for my vertical scroll frame widget here
        vertScrollStyleFrame = Style()
        vertScrollStyleFrame.configure('vertScrollStyle.TFrame',background='#005b96',foreground='#005b96')

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas,style='vertScrollStyle.TFrame')
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

class toggledFrame(Frame):
		# this is class to create a toggle frame - so that you can hide/expand a certain part of the window
		# from view

	def __init__(self, parent, text='',**options):
		Frame.__init__(self, parent, **options)
		self.show=IntVar()
		self.show.set(0)

		# make a style for my toggle frame widgets here
		toggleStyleFrame = Style()
		toggleStyleFrame.configure('teststyle.TFrame',background='#005b96',foreground='#005b96')
		toggleStyleLabel = Style()
		toggleStyleLabel.configure('teststyle.TLabel',background='#005b96',foreground='white',font=("Helvetica", 16))

		# make the frames and labels for my toggle box here
		self.titleFrame=Frame(self,style='teststyle.TFrame')
		self.titleFrame.pack(fill=X, expand=1)
		Label(self.titleFrame, text=text,style='teststyle.TLabel').pack(side=LEFT, fill=X, expand=1,padx=5)
		self.toggleButton=Checkbutton(self.titleFrame, width=2,text='+', command=self.toggle,
										  variable=self.show, style='Toolbutton')
		self.toggleButton.pack(side=LEFT)
		self.subFrame=Frame(self, relief=SUNKEN,borderwidth=1,style='teststyle.TFrame')

	def toggle(self):
		if bool(self.show.get()):
		    self.subFrame.pack(fill=X, expand=1)
		    self.toggleButton.configure(text='-')
		else:
		    self.subFrame.forget()
		    self.toggleButton.configure(text='+')

class DynamicLabel(tk.Label):
    def __init__(self, *args, **kwargs):
        tk.Label.__init__(self, *args, **kwargs)

        # clone the font, so we can dynamically change
        # it to fit the label width
        font = self.cget("font")
        base_font = tkFont.nametofont(self.cget("font"))
        self.font = tkFont.Font()
        self.font.configure(**base_font.configure())
        self.configure(font=self.font)

        self.bind("<Configure>", self._on_configure)

    def _on_configure(self, event):
        text = self.cget("text")

        # first, grow the font until the text is too big,
        size = self.font.actual("size")
        while size < event.width:
            size += 1
            self.font.configure(size=size)

        # ... then shrink it until it fits
        while size > 1 and self.font.measure(text) > event.width:
            size -= 1
            self.font.configure(size=size)
