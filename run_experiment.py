import tkinter as tk

# import to measure time elapsed between clicks
import time

# imports for graphs
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

"""
===THIS IS COMMENTED BECAUSE THE CONNECTION DATA IS IN AN UNCOMMITTED FILE===
# TODO: Uncomment this for the final experiment
# import to connect to Google Sheets API
from connect import connect


# connect() uses Google Sheets API to connect to 
# the spreadsheet that we'll write to
sheet = connect()

# Writes the data entered in the beginning of the 
# experment to our Google Sheet
def write_participants_data(row_to_write):
    global sheet
    sheet.append_row(row_to_write)  
"""

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


##################### Events to be detected on a graph #####################
def on_mouse_down(event):
    global mouse_is_pressed
    global start_time
    print("you clicked")
    mouse_is_pressed = True
    start_time = time.time()


def on_mouse_up(event):
    global mouse_is_pressed
    global start_time
    print("you released")
    mouse_is_pressed = False
    end_time = time.time()
    print("Time elapsed:", end_time - start_time)


def on_mouse_hover(event):
    global cursor_coord
    # this frequently updates the cursor location
    cursor_coord["x"] = event.xdata
    cursor_coord["y"] = event.ydata

##########################################

# A periodicl task to collect the cursor position over time
def task():
    global cursor_coord
    if mouse_is_pressed:
        print(cursor_coord)
        # TODO:
        # if mouse is pressed, check where the cursor lies,
        # check if it's near the example function
        # and then do something smart with that information.
    else:
        print("no")
    root.after(1000, task)

# Starts the experiment and calls the method that 
# writes the data to our Google Sheet
def start_experiment(name, age, device, difficulty, order, event):
    global cursor_coord
    global mouse_is_pressed
    # write_participants_data([name, age, device, difficulty, order])
    window = tk.Toplevel()
    window.title("Task window")
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

    canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    mouse_is_pressed = False
    # cursor_coord is where last logged mouse coordinates will be stored,
    # is (0, 0) by default
    cursor_coord = {"x": 0, "y": 0}    

    canvas.mpl_connect("button_press_event", on_mouse_down)
    canvas.mpl_connect("button_release_event", on_mouse_up)
    canvas.mpl_connect("motion_notify_event", on_mouse_hover)

    window.after(1000, task)

# Creates the UI for entering the participants data
# and for mode selection 
def create_menu(root):
    # Entering the participants name
    name_label = tk.Label(text='Participants name:')
    name_label.grid(row=0, column=0)
    name = tk.StringVar()
    name_entry = tk.Entry(root,textvariable=name, width=30)
    name_entry.grid(row=0, column=1)

    # Entering the participants age
    age_label = tk.Label(text='Participants age:')
    age_label.grid(row=1, column=0)
    age = tk.StringVar()
    age_entry = tk.Entry(root,textvariable=age, width=30)
    age_entry.grid(row=1, column=1)
    
    # Entering the participants input device
    AVAILABLE_DEVICES = ["Mouse", "Trackpad", "Graphic tablet"]
    device_label = tk.Label(text='Input device:')
    device_label.grid(row=2, column=0)  
    device = tk.StringVar(root)
    device.set(AVAILABLE_DEVICES[0])
    device_entry = tk.OptionMenu(root, device, *AVAILABLE_DEVICES)
    device_entry.grid(row=2, column=1)

    # Entering the difficulty
    DIFFICULTY = ["Easy", "Medium", "Hard"]
    difficulty_label = tk.Label(text='Difficulty:')
    difficulty_label.grid(row=3, column=0)  
    difficulty = tk.StringVar(root)
    difficulty.set(DIFFICULTY[0])
    difficulty_entry = tk.OptionMenu(root, difficulty, *DIFFICULTY)
    difficulty_entry.grid(row=3, column=1)

    # Choosing the order of tasks
    ORDER = ["(1, 2, 3)", "(1, 3, 2)", "(2, 3, 1)", "(2, 1, 3)", "(3, 1, 2)", "(3, 2, 1)"]
    order_label = tk.Label(text='Order of tasks:')
    order_label.grid(row=4, column=0)  
    order = tk.StringVar(root)
    order.set(ORDER[0])
    order_entry = tk.OptionMenu(root, order, *ORDER)
    order_entry.grid(row=4, column=1)

    # Button that starts the experiment
    b = tk.Button(root, text="Start experiment")
    b.grid(row=5, column=0, columnspan=2)    
    b.bind("<Button-1>", lambda e: start_experiment(name.get(), age.get(), device.get(), difficulty.get(), order.get(), e))

# Call for main
if __name__ == "__main__":

    root = tk.Tk()
    root.title("Experiment parameters")

    create_menu(root)
    
    root.mainloop()