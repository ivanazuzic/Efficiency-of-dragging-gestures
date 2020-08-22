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
            kappa = abs(f**2 + 2 * fder**2 - f * fderder) / ((fder**2 + f**2) ** (3 / 2)) + 1
        return kappa

    def provide_function_y(self, difficulty, task, x, test_index):
        if(
            test_index > len(self.function_array) or
            difficulty > len(self.function_array[test_index]) or
            task > len(self.function_array[test_index][difficulty])
        ):
            return None

        return self.calculate_y(self.function_array[test_index][difficulty][task], x)

    def provide_function(self, difficulty, task, test_index):
        if(
            test_index > len(self.function_array) or
            difficulty > len(self.function_array[test_index]) or
            task > len(self.function_array[test_index][difficulty])
        ):
            return None

        return self.function_array[test_index][difficulty][task]()

    # ======= ALL THE FUNCTIONS =======
    # These are the functions we're plotting.
    # They return the values array y=f(x)
    # for the given values x.

    # Difficulty: EASY
    ##### Cartesian Coordinates #####    
    def function_curve_d1_t1(self):
        f = 0.2 * (self.x + 1.5)
        return f

    ##### Cartesian Coordinates #####    
    def function_curve_d1_t2(self):
        f = (sp.exp(-self.x + 5) + sp.exp(self.x)) / 2**8 + 0.2
        return f

    ##### Cartesian Coordinates #####    
    def function_curve_d1_t3(self):
        f = sp.sqrt(self.x + 0.001) / 1.2 + 0.2
        return f

    ##### Cartesian Coordinates #####        
    def function_curve_d1_t4(self):
        f = -0.2 * (self.x) + 1.5
        return f

    ##### Polar Coordinates #####
    def function_curve_d1_t5(self):
        f = self.make_sin_rosette(1.8, 0.3, 2)
        return f

    ##### Polar Coordinates #####
    def function_curve_d1_t6(self):
        f = self.make_spiral(1.6, 0.1)
        return f

    ##### Polar Coordinates #####
    def function_curve_d1_t7(self):
        f = self.make_spiral(1.8, 0)
        return f
    
    ##### Polar Coordinates #####
    def function_curve_d1_t8(self):
        f = self.make_sin_rosette(1.75, -0.1, 3)
        return f

    # Difficulty: MEDIUM

    ##### Cartesian Coordinates #####    
    def function_curve_d2_t1(self):
        f = sp.sin(2.5 * self.x) * 0.75 + 1.25
        return f

    ##### Cartesian Coordinates #####    
    def function_curve_d2_t2(self):
        f = self.make_sine_gaussian(-1, -3, 1.7, 5, 5) + 1.25
        return f

    ##### Cartesian Coordinates #####    
    def function_curve_d2_t3(self):
        f = self.make_sine_gaussian(1, -2, 2, 4, 50) + 1.25
        return f

    ##### Cartesian Coordinates #####    
    def function_curve_d2_t4(self):
        f = self.make_fourier(0.25, 0.6, 2, -0.3)
        return f

    ##### Polar Coordinates #####
    def function_curve_d2_t5(self):
        f = self.make_sin_rosette(1.2, -0.75, 2)
        return f

    ##### Polar Coordinates #####
    def function_curve_d2_t6(self):
        f = self.make_bean(1.4, -0.7, 1.5, 3.3)
        return f

    ##### Polar Coordinates #####
    def function_curve_d2_t7(self):
        f = self.make_bean(1.3, 0.7, 3, 1)
        return f
    
    ##### Polar Coordinates #####
    def function_curve_d2_t8(self):
        f = self.make_sin_rosette(1.2, -0.75, 2.3)
        return f

    # Difficulty: HARD
    ##### Cartesian Coordinates #####    
    def function_curve_d3_t1(self):
        f = self.make_fourier(0.29, 1.5, 0.15, 0.3)
        return f

    ##### Cartesian Coordinates #####    
    def function_curve_d3_t2(self):
        f = self.make_sine_gaussian(1, -2.5, 3, 6, 2.5) + 1.25
        return f

    ##### Cartesian Coordinates #####    
    def function_curve_d3_t3(self):
        f = self.make_sinc(12, 6, 8.3) + 1.25
        return f

    ##### Cartesian Coordinates #####    
    def function_curve_d3_t4(self):
        f = self.make_fourier(-0.17, -0.5, -1.5, 0.35)
        return f    

    ##### Polar Coordinates #####
    def function_curve_d3_t5(self):
        f = self.make_sin_rosette(1.3, -0.6, 6.1)
        return f

    ##### Polar Coordinates #####
    def function_curve_d3_t6(self):
        f = self.make_bean(1.4, -0.7, 5.1, 3)
        return f

    ##### Polar Coordinates #####
    def function_curve_d3_t7(self):
        f = self.make_sin_rosette(1.3, -0.7, 5.1)
        return f
    
    ##### Polar Coordinates #####
    def function_curve_d3_t8(self):
        f = self.make_bean(1.4, -0.75, 3.1, -5)
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

    def make_fourier(self, a, b, c, d = 1):
        return (sp.sin(self.x /a) + sp.sin(self.x / b) + sp.cos(self.x / c)) * d + 1.25  

    def make_bean(self, a, b, c, d):
        return a + b * sp.sin(c * self.x) * sp.cos(d * self.x)

    def make_sin_rosette(self, a, b, c):
        return a + b * sp.sin(c * self.x)

    def make_spiral(self, a, b):
        return a + b * self.x

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