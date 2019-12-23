import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

##################### function init #####################

x_range = {
    # start point and end point on which f(x) is defined
    "start": 0,
    "end": 50,
}


def function_curve(x):
    # this is the function we're plotting.
    # it returns its value y=f(x) based on the value of the
    # given x.

    # this example function has two parts,
    # equally divided across x_range.

    diff = np.abs(x_range["end"] - x_range["start"])
    divide_point = (diff / 2.0) + x_range["start"]

    if(x > divide_point):
        return 5 * np.sin(x)
    else:
        return x * x - 15 * x


##########################################


root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)

# the following line always produces 100 equally spread points on the x_range
t = np.arange(
    x_range["start"],
    x_range["end"],
    np.abs(x_range["end"] - x_range["start"]) / 100.00
)

y = np.zeros(len(t))

for i in range(len(y)):
    y[i] = function_curve(t[i])  # calculate y for each generated t


fig.add_subplot(111).plot(t, y)  # plot the generated t and y

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

mouse_is_pressed = False
# cursor_coord is where last logged mouse coordinates will be stored,
# is (0, 0) by default
cursor_coord = {"x": 0, "y": 0}


def on_mouse_down(event):
    global mouse_is_pressed
    print("you clicked")
    mouse_is_pressed = True


def on_mouse_up(event):
    global mouse_is_pressed
    print("you released")
    mouse_is_pressed = False


def on_mouse_hover(event):
    # this frequently updates the cursor location
    cursor_coord["x"] = event.xdata
    cursor_coord["y"] = event.ydata


canvas.mpl_connect("button_press_event", on_mouse_down)
canvas.mpl_connect("button_release_event", on_mouse_up)
canvas.mpl_connect("motion_notify_event", on_mouse_hover)


def task():
    if mouse_is_pressed:
        print(cursor_coord)
        # TODO:
        # if mouse is pressed, check where the cursor lies,
        # check if it's near the example function
        # and then do something smart with that information.
    else:
        print("no")
    root.after(1000, task)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

root.after(1000, task)
tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
