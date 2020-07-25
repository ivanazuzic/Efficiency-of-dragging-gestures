import numpy as np
import sympy as sp

class FunctionProvider:
    def __init__(self):
        self.x = sp.Symbol("x")

        self.function_array = [
            # functions for test 1
            [
                [self.function_curve_d1_t1, self.function_curve_d1_t2],  # EASY
                [self.function_curve_d2_t1, self.function_curve_d2_t2],  # MEDIUM
                [self.function_curve_d3_t1, self.function_curve_d3_t2],  # HARD
            ],

            # functions for test 2
            [
                [self.function_curve_d1_t3, self.function_curve_d1_t4],  # EASY
                [self.function_curve_d2_t3, self.function_curve_d2_t4],  # MEDIUM
                [self.function_curve_d3_t3, self.function_curve_d3_t4],  # HARD
            ],
            # functions for test 3
            [
                [self.function_curve_d1_t5, self.function_curve_d1_t6],  # EASY
                [self.function_curve_d2_t5, self.function_curve_d2_t6],  # MEDIUM
                [self.function_curve_d3_t5, self.function_curve_d3_t6],  # HARD
            ],
            # functions for test 4
            [
                [self.function_curve_d1_t7, self.function_curve_d1_t8],  # EASY
                [self.function_curve_d2_t7, self.function_curve_d2_t8],  # MEDIUM
                [self.function_curve_d3_t7, self.function_curve_d3_t8],  # HARD
            ],
        ]

    def get_function_curvature(self, difficulty, task, test_index):
        # gets index of difficulty for the function
        kappa = None
        if(
            test_index > len(self.function_array) or
            difficulty > len(self.function_array[test_index]) or
            task > len(self.function_array[test_index][difficulty])
        ):
            return None

        f = self.function_array[test_index][difficulty][task]()
        fder = f.diff(self.x)
        fderder = fder.diff(self.x)

        if is_cartesian((test_index)):
            kappa = sp.sqrt((fderder)**2) / ((1 + (fder)**2)**(3 / 2)) + 1
        else:
            # kappa for polar coordinates
            kappa = abs(f**2 + 2 * fder**2 - f * fderder) / ((fder**2 + f**2) ** (3 / 2))
        return kappa

    def provide_function_y(self, difficulty, task, x, test_index):
        if(
            test_index > len(self.function_array) or
            difficulty > len(self.function_array[test_index]) or
            task > len(self.function_array[test_index][difficulty])
        ):
            return None

        return self.calculate_y(self.function_array[test_index][difficulty][task], x)

    # ======= ALL THE FUNCTIONS =======
    # These are the functions we're plotting.
    # They return the values array y=f(x)
    # for the given values x.

    # Difficulty: EASY
    # Linear function
    def function_curve_d1_t1(self):
        f = 0.5 * (self.x - 2.5)
        return f

    # Exponential function
    def function_curve_d1_t2(self):
        f = sp.exp(self.x) / 2**6 - 1
        return f

    # Square root function
    def function_curve_d1_t3(self):
        f = sp.sqrt(self.x) - 0.5
        return f

    # Linear function
    def function_curve_d1_t4(self):
        f = -0.5 * (self.x - 2.5)
        return f

    ##### Polar Coordinates #####
    def function_curve_d1_t5(self):
        f = 1 - self.x
        return f

    ##### Polar Coordinates #####
    def function_curve_d1_t6(self):
        f = sp.cos(self.x)
        return f

    ##### Polar Coordinates #####
    def function_curve_d1_t7(self):
        f = 0.5 + 0.5 * self.
        return f
    
    ##### Polar Coordinates #####
    def function_curve_d1_t8(self):
        f = sp.sin(self.x)
        return f

    # Difficulty: MEDIUM

    # Sine
    def function_curve_d2_t1(self):
        f = sp.sin(self.x * 2)
        return f

    # Sine Gaussian
    def function_curve_d2_t2(self):
        f = self.make_sine_gaussian(2, -2, 1, 3, 50)
        return f

    # Sine Gaussian
    def function_curve_d2_t3(self):
        f = self.make_sine_gaussian(-1.5, -2, 0.8, 5, 30)
        return f

    # High degree polinome
    def function_curve_d2_t4(self):
        f = (self.x - 0.5) * (self.x - 1.7) * (self.x - 3.6) * (self.x - 4.6) / 7 - 1
        return f

    ##### Polar Coordinates #####
    def function_curve_d2_t5(self):
        f = sp.cos(self.x)
        return f

    ##### Polar Coordinates #####
    def function_curve_d2_t6(self):
        f = sp.cos(self.x)
        return f

    ##### Polar Coordinates #####
    def function_curve_d2_t7(self):
        f = sp.sin(self.x)
        return f
    
    ##### Polar Coordinates #####
    def function_curve_d2_t8(self):
        f = sp.sin(self.x)
        return f

    # Difficulty: HARD
    # Fourier
    def function_curve_d3_t1(self):
        f = self.make_fourier(0.5, 2, 0.2)
        return f

    # Sine Gaussian
    def function_curve_d3_t2(self):
        f = self.make_sine_gaussian(2, -2.5, 3, 5, 2.5)
        return f

    # Sinc
    def function_curve_d3_t3(self):
        f = self.make_sinc(17, 5, 6.1)
        return f

    # Sine Gaussian
    def function_curve_d3_t4(self):
        f = self.make_sine_gaussian(2, -1, 8, 5, 2.5)
        return f    

    ##### Polar Coordinates #####
    def function_curve_d3_t5(self):
        f = sp.cos(self.x) + sp.sin(self.x)
        return f

    ##### Polar Coordinates #####
    def function_curve_d3_t6(self):
        f = sp.cos(self.x) + sp.sin(self.x)
        return f

    ##### Polar Coordinates #####
    def function_curve_d3_t7(self):
        f = sp.sin(self.x) + sp.sin(self.x)
        return f
    
    ##### Polar Coordinates #####
    def function_curve_d3_t8(self):
        f = sp.sin(self.x) + sp.sin(self.x)
        return f

    def calculate_y(self, function, x_arr):
        y = np.zeros(len(x_arr))
        # get the function for plotting
        f = sp.lambdify(self.x, function(), "numpy")

        for i in range(0, len(x_arr)):
            # calculate y for each given y
            y[i] = f(x_arr[i])

        return y

    def make_sine_gaussian(self, a, b, c, d, f):
        return a * sp.exp(-(self.x + b)**2/c) * sp.sin(d * (self.x + f))

    def make_sinc(self, a, b, c):
        return a*sp.sin(b*(self.x-c)) / (b*(self.x-c))

    def make_fourier(self, a, b, c):
        return sp.sin(self.x /a) + sp.sin(self.x / b) + sp.cos(self.x / c) - 1


def is_cartesian(test_index):
    return test_index == 0 or test_index == 1

"""
# Testing area

x = np.arange(-100,100,1)
fp = FunctionProvider()
y = fp.provide_function(3, 1, x)

plt.plot(y)
plt.ylabel('test')
plt.show()
"""