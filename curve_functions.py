import math
import numpy as np
import matplotlib.pyplot as plt

class FunctionProvider:
    def __init__(self):
        self.x_range = {
            # start point and end point on which f(x) is defined
            "start": 0,
            "end": 50,
        }

    def provide_function(self, difficulty, task, x):
        if difficulty == 1 and task == 1:
            return self.function_curve_d1_t1(x)
        if difficulty == 1 and task == 2:
            return self.function_curve_d1_t2(x)
        if difficulty == 1 and task == 3:
            return self.function_curve_d1_t3(x)

        if difficulty == 2 and task == 1:
            return self.function_curve_d2_t1(x)
        if difficulty == 2 and task == 2:
            return self.function_curve_d2_t2(x)
        if difficulty == 2 and task == 3:
            return self.function_curve_d2_t3(x)

        if difficulty == 3 and task == 1:
            return self.function_curve_d3_t1(x)
        if difficulty == 3 and task == 2:
            return self.function_curve_d3_t2(x)
        if difficulty == 3 and task == 3:
            return self.function_curve_d3_t3(x)

    # ======= ALL THE FUNCTIONS =======
    # These are the functions we're plotting.
    # They return the values array y=f(x) 
    # for the given values x.

    # Difficulyt: EASY

    # Linear function
    def function_curve_d1_t1(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = 15 / 13 * x + 2
            i += 1

        return y

    # Exponential function
    def function_curve_d1_t2(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = math.exp(x / 10) 
            i += 1

        return y

    # Square root function
    def function_curve_d1_t3(self, x_arr):
        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = math.sqrt(x) * 25 
            i += 1

        return y

    # Difficulyt: MEDIUM

    # Logarithm
    def function_curve_d2_t1(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = 50 * math.sin(x / 3) + 100
            i += 1

        return y

    # Quadratic function
    def function_curve_d2_t2(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = (x - 15) * (x - 40) * (x - 5) * (x - 50) / 1000 + 80
            i += 1

        return y

    # High degree polinome
    def function_curve_d2_t3(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = (x - 1) * (x - 15) * (x - 25) * (x - 35) * (x - 49) / 20000 + 100
            i += 1

        return y

    # Difficulty: HARD

    # This function has two parts,
    # equally divided across x_range.
    def function_curve_d3_t1(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in range(len(y)):
            # calculate y for each generated t
            y[i] = 50 * np.sin(x / 10) + 50 * np.cos(x / 5) + 20 * np.sin(x / 4) + 100
            i += 1

        return y

    # This function has two parts,
    # equally divided across x_range.
    def function_curve_d3_t2(self, x_arr):

        y = np.zeros(len(x_arr))
        divide_point = 6 * math.pi
        i = 0
        for x in x_arr:
            # calculate y for each generated t
            if(x < divide_point):
                y[i] = 80 * math.sin(x / 2) + 100
            else:
                y[i] = (x - divide_point) * (x - 35) * (x - 43) / 17 + 100
            i += 1

        return y

    # Tangens
    def function_curve_d3_t3(self, x_arr):

        y = np.zeros(len(x_arr))

        divide_point1 = 4 * math.pi
        divide_point2 = 10 * math.pi

        i = 0
        for x in x_arr:
            # calculate y for each given x
            if x < divide_point1:
                y[i] = 6 * (x - divide_point1)
            elif x < divide_point2:
                y[i] = 50 * math.sin(x / 2)
            else:
                y[i] = (x - divide_point2) * (x - divide_point2 - 17) * (x - divide_point2 - 5) * (x - divide_point2 - 9) / 100
            y[i] *= 2
            y[i] += 100
            i += 1

        print(y) 

        return y

"""
# Testing area

x = np.arange(-100,100,1)
fp = FunctionProvider()
y = fp.provide_function(3, 1, x)

plt.plot(y)
plt.ylabel('test')
plt.show()
"""