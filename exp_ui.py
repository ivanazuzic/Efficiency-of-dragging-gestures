import tkinter as tk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

from curve_functions import FunctionProvider

class ExperimentWindow(tk.Frame):
    def __init__(self, parent, difficulty, order, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.difficulty = difficulty
        self.order = order

        self.SAMPLE_TIMEOUT = 10  # how much milliseconds pass between sampling

        self.x_range = {
            # start point and end point on which f(x) is defined
            "start": 0,
            "end": 50,
        }

        self.window = tk.Toplevel()
        self.window.title("Task window")

        self.fig = Figure(figsize=(9, 7), dpi=100)

        # the following line always produces 100 equally spread points on the x_range
        self.t = np.arange(
            self.x_range["start"],
            self.x_range["end"],
            np.abs(self.x_range["end"] - self.x_range["start"]) / 100.00
        )

        self.fp = FunctionProvider()

        self.y = np.zeros(len(self.t))
        self.y = self.fp.provide_function(difficulty, order[0], self.t)

        self.graph = self.fig.add_subplot(111)  # this is the subplot on which we draw
        self.graph.set_xlim([-40, 90]) # limiting the x axis range
        self.graph.set_ylim([-80, 300]) # limiting the y axis range
        self.graph.plot(self.t, self.y)  # plot the generated t and y

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)

        self.is_mouse_pressed = False
        # cursor_coord holds the last (ultimate) logged cursor coordinate,
        # is (0, 0) by default
        self.cursor_coord = {"x": 0, "y": 0}

        self.cursor_coord = {"x": 0, "y": 0}

        self.canvas.mpl_connect("button_press_event", self.on_mouse_down)
        self.canvas.mpl_connect("button_release_event", self.on_mouse_up)
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_hover)

        self.button = tk.Button(master=self.window, text="Quit", command=self._quit)
        self.button.grid(row=2, column=0)

        self.window.after(self.SAMPLE_TIMEOUT, self.task)

        # Setting the windows size and initial position
        width = 900
        height = 700
        self.window.geometry('{}x{}+{}+{}'.format(width, height, 10, 10))

        # Setting the screen state to be toggleable
        # By default the screen is small 
        self.screen_state = False
        self.window.attributes("-fullscreen", self.screen_state)
        self.window.bind("<Escape>", self.toggle_fullscreen)


    # Toggles to full screen and back
    def toggle_fullscreen(self, event=None):
        self.screen_state = not self.screen_state  # Just toggling the boolean
        self.window.attributes("-fullscreen", self.screen_state)
        print("Toggle")
        return "break"

    
    def _quit(self):
        self.window.quit()     # stops mainloop
        self.window.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def task(self):
        if self.is_mouse_pressed:
            # TODO:
            # if mouse is pressed, check where the cursor lies,
            # check if it's near the example function
            # and then do something smart with that information.

            # plotting a point on the subplot
            # at the current cursor coordinates (x, y).
            self.graph.scatter(
                self.cursor_coord["x"],
                self.cursor_coord["y"],
                # make it wider than the original curve
                linewidth=2,
                # give it a subtle color to avoid visual clutter
                # and make it 80% visible
                color=(0.7, 0.8, 0.7, 0.8)
            )
            self.fig.canvas.draw()  # update the canvas

        else:
            # do something if mouse is not pressed...
            pass

        self.window.after(self.SAMPLE_TIMEOUT, self.task)

    def on_mouse_down(self, event):
        print("you clicked")
        self.is_mouse_pressed = True


    def on_mouse_up(self, event):
        print("you released")
        self.is_mouse_pressed = False


    def on_mouse_hover(self, event):
        # this frequently updates the cursor location
        self.cursor_coord["x"] = event.xdata
        self.cursor_coord["y"] = event.ydata