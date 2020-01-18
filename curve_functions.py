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

        self.function_array = [
            [self.function_curve_d1_t1, self.function_curve_d1_t2],  # EASY
            [self.function_curve_d2_t1, self.function_curve_d2_t2],  # MEDIUM
            [self.function_curve_d3_t1, self.function_curve_d3_t2],  # HARD
        ]

    def provide_function(self, difficulty, task, x):
        if(
            difficulty > len(self.function_array) or
            task > len(self.function_array[difficulty])
        ):
            return None

        return self.function_array[difficulty][task](x)

    # ======= ALL THE FUNCTIONS =======
    # These are the functions we're plotting.
    # They return the values array y=f(x) 
    # for the given values x.


    # Difficulty: EASY
    # Linear function
    def function_curve_d1_t1(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = 0.5 * (x - 2.5)
            i += 1

        return y

    # Exponential function
    def function_curve_d1_t2(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = math.exp(x) / 2**6 - 1
            i += 1

        return y

    # Square root function
    def function_curve_d1_t3(self, x_arr):
        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = math.sqrt(x)
            i += 1

        return y

    # Difficulyt: MEDIUM

    # Logarithm
    def function_curve_d2_t1(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = math.sin(x * 2)
            i += 1

        return y

    # Quadratic function
    def function_curve_d2_t2(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = (x - 0.5) * (x - 1.7) * (x - 3.6) * (x - 4.6) / 7 - 1
            i += 1

        return y

    # High degree polinome
    def function_curve_d2_t3(self, x_arr):

        y = np.zeros(len(x_arr))

        i = 0
        for x in x_arr:
            # calculate y for each given x
            y[i] = (x - 0.3) * (x - 2) * (x - 3.4) * (x - 4) * (x - 4.5) / 2**2
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
            y[i] = np.sin(x/ 100) + np.sin(x / 477) + np.cos(x / 50) - 1
            i += 1

        return y

    # This function has two parts,
    # equally divided across x_range.
    def function_curve_d3_t2(self, x_arr):

        y = np.zeros(len(x_arr))
        i = 0
        for x in x_arr:
            # calculate y for each generated t
            # FIXME: place another function here...
            y[i] = 0
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