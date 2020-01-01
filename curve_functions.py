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
        print(x)
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
            y[i] = 15 / 13 * x - 5
            i += 1

        return y

    # Exponential function
    def function_curve_d1_t2(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = math.exp(x)
            i += 1

        return y

    # Parabolic function
    def function_curve_d1_t3(self, x_arr):
        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = - 200 * x * x - 800 * x - 3
            i += 1

        return y

    # Difficulyt: MEDIUM

    # Logarithm
    def function_curve_d2_t1(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            if x <= 0:
                # has to be greater than zero because of the logarithm domain
                continue
            # calculate y for each given x
            y[i] = 50 * math.log(x)
            i += 1

        return y

    # Cubic function
    def function_curve_d2_t2(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = x * x * x
            i += 1

        return y

    # High degree polinome: x^5 * 3 - x^4
    def function_curve_d2_t3(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = x*x*x*x*x * 3 - x*x*x*x
            i += 1

        return y

    # Difficulyt: HARD

    # This function has two parts,
    # equally divided across x_range.
    def function_curve_d3_t1(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in range(len(y)):
            # calculate y for each generated t

            diff = np.abs(self.x_range["end"] - self.x_range["start"])
            divide_point = (diff / 2.0) + self.x_range["start"]

            if(x > divide_point):
                y[i] = 5 * np.sin(x)
            else:
                y[i] = x * x - 15 * x
            i += 1

        return y

    # This function has two parts,
    # equally divided across x_range.
    def function_curve_d3_t2(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in range(len(y)):
            # calculate y for each generated t

            diff = np.abs(self.x_range["end"] - self.x_range["start"])
            divide_point = (diff / 2.0) + self.x_range["start"]

            if(x > divide_point):
                y[i] = 5 * math.tan(x)
            else:
                y[i] = x * x * x - 7 * x * x - 15 * x
            i += 1

        return y

    # Tangens
    def function_curve_d3_t3(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = math.tan(x)
            i += 1

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