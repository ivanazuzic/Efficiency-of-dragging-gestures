import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Implement the default Matplotlib key bindings.
from matplotlib.figure import Figure

import random, math
import numpy as np
import time

from curve_functions import FunctionProvider, is_cartesian
from backing_up_locally import *

# ~~~~~~~~~
#===THIS IS COMMENTED BECAUSE THE CONNECTION DATA IS IN AN UNCOMMITTED FILE===
# TODO: Uncomment this for the final experiment
# import to connect to Google Sheets API
from connect import connect
#import to get the current timestamp
import time as time
# ~~~~~~~~~

""" how many times a curve function can repeat"""
NUM_OF_CYCLES = 2
NUM_OF_DIFFICULY_CATEGORIES = 3
NUM_OF_FUNCTIONS_PER_DIFF = 2
""" For experiment with index 0,
test 0 and 2 are used. For experiment with index 1, tests 1 and 3 are used.
0,1 - cartesian tests; 2,3 - polar tests """
TESTS_IN_EXPERIMENT = [[0, 2], [1, 3]]

class ExperimentWindow(tk.Frame):
    def __init__(
        self,
        parent,
        participant_name,
        age,
        device,
        experiment_mode,
        # difficulty,
        # order,
        *args,
        **kwargs
    ):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.participant_name = participant_name
        self.age = age
        self.device = device
        self.experiment_mode = experiment_mode
        # self.difficulty = difficulty
        # self.function_order = order

        self.x_drawn = []
        self.y_drawn = []
        self.drawing_time = 0

        # ~~~~~~~~~
        # connect() uses Google Sheets API to connect to 
        # the spreadsheet that we'll write to
        # TODO: Uncomment this for the final experiment
        self.sheet = connect()
        # ~~~~~~~~~
        self.function_order, self.projection_order = self.generate_random_function_order()
        # this is the index of the function we're currently plotting
        # starting from the first element in order[]
        self.current_function_index = 0

        self.window = tk.Toplevel()
        self.window.title("Task window")

        self.fig = Figure(figsize=(9, 7), dpi=100)
        # A tk.DrawingArea.
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.init_graph()

        self.fp = FunctionProvider()
        self.y = np.zeros(len(self.t))

        # these two are used for measuring how much time
        # it took the user to follow the function trajectory
        self.time_start = None
        self.time_end = None

        self.init_plot(self.current_function_index)

        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=10)

        self.is_mouse_pressed = False
        # cursor_coord holds the last (ultimate)
        # and penultimate logged cursor coordinate
        self.cursor_coord = [
            {"x": None, "y": None},  # penultimate
            {"x": None, "y": None},  # ultimate
        ]

        self.canvas.mpl_connect("button_press_event", self.on_mouse_down)
        self.canvas.mpl_connect("button_release_event", self.on_mouse_up)
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_hover)

        # this is the "Undo" button
        # EDIT: NOT NECESSARY
        # self.button_undo = tk.Button(
        #     master=self.window,
        #     text='Undo',
        #     command=self.undo_gesture
        # )
        # self.button_undo.grid(row=0, column=1)

        # this is the "Next" button.
        # it is disabled in the beginning - it should not be allowed
        # to proceed to the next function without at least
        # clicking on this one
        self.button_next = tk.Button(
            master=self.window,
            text='Next',
            command=self.next_function,
            state="disabled"
        )
        self.button_next.grid(row=1, column=1)

        # this is the "Quit" button
        self.button_quit = tk.Button(
            master=self.window,
            text="Quit",
            command=self._quit
        )
        self.button_quit.grid(row=2, column=1)

        self.cur_coord_stringvar = tk.StringVar()
        self.cur_coord_stringvar.set("")
        self.cur_coord_label = tk.Label(master=self.window, textvariable=self.cur_coord_stringvar)
        self.cur_coord_label.grid(row=3, column=1)

        # self.window.after(self.SAMPLE_TIMEOUT, self.task)

        # Setting the windows size and initial position
        width = 1000
        height = 700
        self.window.geometry('{}x{}+{}+{}'.format(width, height, 10, 10))

        # Setting the screen state to be toggleable
        # By default the screen is small
        self.screen_state = False
        self.window.attributes("-fullscreen", self.screen_state)
        self.window.bind("<Escape>", self.toggle_fullscreen)

    def init_graph(self):
        x_range = {}
        graph = None
        if self.is_plot_cartestian():
            # init cartesian graph
            x_range = {
                # start point and end point on which f(x) is defined
                "start": 0,
                "end": 5,
            }
            graph = self.fig.add_subplot(111)
            # limiting the x axis range
            # but only if coordinates are Cartesian
            graph.set_xlim([
                x_range["start"] - (x_range["end"] - x_range["start"]) / 6,
                x_range["end"] + (x_range["end"] - x_range["start"]) / 6
            ])
            # limiting the y axis range
            graph.set_ylim([-2.5, 2.5])
        else:
            # init polar graph
            x_range = {
                # start point and end point on which f(x) is defined
                "start": 0,
                "end": 2 * math.pi,
            }
            graph = self.fig.add_subplot(111, projection="polar")
            # if the coordinates are polar,
            # make the y (which is r in polar) larger
            graph.set_ylim([-1.2, 1.8])
            # this removes the radius (r)
            graph.set_yticks([])

        self.x_range = x_range
        # the following line always produces
        # 1000 equally spread points on the x_range
        self.t = np.linspace(
            self.x_range["start"],
            self.x_range["end"],
            10000
        )
        self.graph = graph

    # Toggles to full screen and back
    def toggle_fullscreen(self, event=None):
        self.screen_state = not self.screen_state  # Just toggling the boolean
        self.window.attributes("-fullscreen", self.screen_state)
        return "break"

    def _quit(self):
        self.window.destroy()

    def undo_gesture(self):
        # this is called when the user wants to undo their
        # current trajectory.

        # first, restore the original background
        self.fig.canvas.restore_region(self.static_background)
        self.fig.canvas.draw()

        # now that the old background is restored,
        # reset the dynamic background to be equal to the static one
        # (as it is in the very beginning)
        self.dynamic_background = self.fig.canvas.copy_from_bbox(
            self.graph.bbox
        )

        # reset the current time
        self.time_start = None
        self.time_end = None

        # make the "Next" button unuseable
        if self.button_next["state"] == "normal":
            self.button_next["state"] = "disabled"

        # delete the currently logged coordinates
        delete_file(
            self.participant_name,
            self.get_current_function_test_mode(),
            self.device,
            self.function_order,
            self.projection_order,
            self.current_function_index
        )

        # clear the list of currently drawn coordinates
        self.x_drawn = []
        self.y_drawn = []

    def init_plot(self, plot_index):
        # this function initialises the plot
        self.time_start = None
        self.time_end = None

        # delete what is currently drawn
        # we must delete the entire axes because their projection changes at runtime
        self.fig.delaxes(self.graph)
        self.init_graph()

        difficulty = int(self.function_order[plot_index] / 2)
        task = int(self.function_order[plot_index] % 2)

        self.y = self.fp.provide_function_y(
            difficulty,
            task,
            self.t,
            self.get_current_function_test_mode()
        )

        # this is for getting function ID
        # self.fp.get_function_analysis(difficulty, task, self.t)

        # these two are used for measuring how much time
        # it took the user to follow the function trajectory
        self.time_start = None
        self.time_end = None

        self.graph.plot(self.t, self.y)  # plot the generated t and y            
        self.canvas.draw()

        # store the background of the current canvas
        # so that we don't have to repeatedly redraw it
        # when plotting the cursor trajectory ---> increases FPS.
        # the static background is constant and holds the original background
        # (which contains only the bare function),
        # but the dynamic background changes while the user is
        # "drawing" (pressing the cursor) along the function trajectory.
        # At the beginning, those two are equal.
        self.static_background = self.fig.canvas.copy_from_bbox(
            self.graph.bbox
        )
        self.dynamic_background = self.fig.canvas.copy_from_bbox(
            self.graph.bbox
        )

    def next_function(self):
        # error calculation
        task = int(self.function_order[self.current_function_index] % 2)
        difficulty = int(self.function_order[self.current_function_index] / 2)
        actual_y = self.fp.provide_function_y(
            difficulty,
            task,
            self.x_drawn,
            self.get_current_function_test_mode()
        )
        error = 0
        for y1, y2 in zip(self.y_drawn, actual_y):
            error += abs(y1 - y2)
        print("Error:", error)
        # ---------

        # ~~~~~~~~~
        # TODO: Uncomment this for the final experiment
        if self.participant_name != "":
            print("Logiram")
            epoch_time = int(time.time())
            ID = self.function_order[self.current_function_index]
            difficulty = ID // 2
            self.sheet.append_row([
                self.participant_name,
                self.age,
                self.device,
                str(self.experiment_mode),
                str(epoch_time),
                str(ID),
                str(difficulty),
                "Cartesian" if self.is_plot_cartestian() else "Polar",
                str(self.drawing_time),
                str(error),
            ])
        # ~~~~~~~~~

        self.current_function_index = (self.current_function_index + 1)
        if(self.current_function_index >= len(self.function_order)):
            # if all of the functions have been tested and
            # there's nothing else to plot,
            # quit the window
            self._quit()
            return
        self.init_plot(self.current_function_index)  # initalise the next plot

        # disable the "Next" button so that the user can't proceed without
        # at least clicking on the new plot.
        self.button_next["state"] = "disabled"

    def task(self):
        if self.is_mouse_pressed:
            # if the mouse is pressed and the "Next" button is disabled,
            # then enable it
            if self.button_next["state"] == "disabled":
                self.button_next["state"] = "normal"

            # TODO:
            # if mouse is pressed, check where the cursor lies,
            # check if it's near the example function
            # and then do something smart with that information.

            if (
                self.cursor_coord[0]["x"] >= self.x_range["start"] and
                self.cursor_coord[0]["x"] <= self.x_range["end"]
            ):
                self.x_drawn.append(self.cursor_coord[0]["x"])
                self.y_drawn.append(self.cursor_coord[0]["y"])

                # Log a coordinate to a local file
                # print(self.participant_name, self.function_order[self.current_function_index], self.cursor_coord[0]["x"], self.cursor_coord[0]["y"])
                write_to_file(
                    self.participant_name,
                    self.experiment_mode,
                    self.device,
                    self.function_order,
                    self.projection_order,
                    self.current_function_index,
                    self.cursor_coord[0]["x"],
                    self.cursor_coord[0]["y"]
                )

            # first, restore the currently saved background
            self.fig.canvas.restore_region(self.dynamic_background)

            # plot (only!) the line that connects the penultimate
            # and ultimate cursor location
            self.graph.draw_artist(
                self.graph.plot(
                    [self.cursor_coord[0]["x"], self.cursor_coord[1]["x"]],
                    [self.cursor_coord[0]["y"], self.cursor_coord[1]["y"]],
                    # make it wider than the original curve
                    linewidth=2,
                    # give it a subtle color to avoid visual clutter
                    # and make it 50% visible
                    color=(0.7, 0.8, 0.7, 0.5),
                    animated=True
                )[0]
            )
            # update the canvas
            self.fig.canvas.blit(self.graph.bbox)
            # store the background again
            self.dynamic_background = self.fig.canvas.copy_from_bbox(
                self.graph.bbox
            )
        else:
            # do something if mouse is not pressed...
            pass

        # each time this is called,
        # update the penultimate cursor location
        self.cursor_coord[0]["x"] = self.cursor_coord[1]["x"]
        self.cursor_coord[0]["y"] = self.cursor_coord[1]["y"]

        # repeat this task in [SAMPLE_TIMEOUT] milliseconds...
        # self.window.after(self.SAMPLE_TIMEOUT, self.task)

    def on_mouse_down(self, event):
        self.undo_gesture()
        self.time_start = time.time()
        print("you clicked")
        self.is_mouse_pressed = True

    def on_mouse_up(self, event):
        self.time_end = time.time()
        print("you released, your time (in seconds): ", self.time_end - self.time_start)
        self.drawing_time = self.time_end - self.time_start
        self.is_mouse_pressed = False

    def on_mouse_hover(self, event):
        self.task()
        # this frequently updates the ultimate cursor location
        if(event.xdata is not None and event.ydata is not None):
            self.cursor_coord[1]["x"] = event.xdata
            self.cursor_coord[1]["y"] = event.ydata
            # change value in current label to display current cursor coordinate
            self.cur_coord_stringvar.set(str(round(event.xdata, 2)) + " " + str(round(event.ydata, 2)))

    def generate_random_function_order(self):
        # ---------------- generating randomised order ---------------- #
        order = []
        # generate multiple passes through all functions
        for cycle in range(NUM_OF_CYCLES):
            # and each projection
            for test in TESTS_IN_EXPERIMENT[self.experiment_mode]:
                # generate 6 numbers to represent a single "pass"
                # through all the functions in specified projection,
                for function in range(NUM_OF_FUNCTIONS_PER_DIFF * NUM_OF_DIFFICULY_CATEGORIES):
                    order.append([function, test])

        # flag that checks if there are two equal consecutive elements in array
        two_equal = True
        while(two_equal):
            # if there are two consecutive elements that are equal,
            # then shuffle the array
            random.shuffle(order)

            two_equal = False
            # check again if there are two equal consecutive elements
            for i in range(1, len(order)):
                if order[i - 1][0] == order[i][0]:
                    two_equal = True
        # # ---------------- !generating randomised order ---------------- #
        order = np.array(order)
        return order[:, 0], order[:, 1]

    def is_plot_cartestian(self):
        return is_cartesian(self.get_current_function_test_mode())

    def get_current_function_test_mode(self): 
        return self.projection_order[self.current_function_index]