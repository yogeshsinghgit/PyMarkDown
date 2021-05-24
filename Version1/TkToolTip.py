import tkinter as tk

class ToolTip:
    def __init__(self,widget,text=None):

        def on_enter(event):
            self.tooltip=tk.Toplevel()
            self.tooltip.overrideredirect(True)
            self.tooltip.geometry(f'+{event.x_root+2}+{event.y_root+2}')

            self.label=tk.Label(self.tooltip,text=self.text)
            self.label.pack()

        def on_leave(event):
            self.tooltip.destroy()

        self.widget=widget
        self.text=text

        self.widget.bind('<Enter>',on_enter)
        self.widget.bind('<Leave>',on_leave)