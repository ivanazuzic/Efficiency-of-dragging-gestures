import numpy as np
import sympy as sp


class FunctionProvider:
    def __init__(self):
        self.x = sp.Symbol("x")

        self.function_array = [
            [self.function_curve_d1_t1, self.function_curve_d1_t2],  # EASY
            [self.function_curve_d2_t1, self.function_curve_d2_t2],  # MEDIUM
            [self.function_curve_d3_t1, self.function_curve_d3_t2],  # HARD
        ]

    def get_function_analysis(self, difficulty, task, x):
        # gets index of difficulty for the function
        if(
            difficulty > len(self.function_array) or
            task > len(self.function_array[difficulty])
        ):
            return None

        f = self.function_array[difficulty][task]()

        fder = f.diff(self.x)
        fderder = fder.diff(self.x)

        kappa = (fderder) / ((1 + (fder)**2)**(3 / 2)) + f
        kappa = sp.sqrt(kappa ** 2)

        print("curvature: ", kappa)
        curvature_integral = sp.integrate(kappa, self.x)

        print(curvature_integral)

        curvature_integral = sp.lambdify(curvature_integral, self.x)
        print(curvature_integral(np.array([0])))
        print(curvature_integral(np.array([5])))

        return 0

    def provide_function_y(self, difficulty, task, x):
        if(
            difficulty > len(self.function_array) or
            task > len(self.function_array[difficulty])
        ):
            return None

        return self.calculate_y(self.function_array[difficulty][task], x)

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
        f = sp.sqrt(self.x)
        return f

    # Difficulty: MEDIUM

    # Logarithm
    def function_curve_d2_t1(self):
        f = sp.sin(self.x * 2)
        return f

    # Quadratic function
    def function_curve_d2_t2(self):
        f = (self.x - 0.5) * (self.x - 1.7) * (self.x - 3.6) * (self.x - 4.6) / 7 - 1
        return f

    # High degree polinome
    def function_curve_d2_t3(self):
        f = (self.x - 0.3) * (self.x - 2) * (self.x - 3.4) * (self.x - 4) * (self.x - 4.5) / 2**2
        return f

    # Difficulty: HARD

    def function_curve_d3_t1(self):
        f = sp.sin(self.x / 100) + sp.sin(self.x / 477) + sp.cos(self.x / 50) - 1
        return f

    def function_curve_d3_t2(self):
        f = 1 + 0 * self.x
        return f

    def function_curve_d3_t3(self):
        f = 2 + 0 * self.x
        return f

    def calculate_y(self, function, x_arr):
        y = np.zeros(len(x_arr))
        # get the function for plotting
        f = sp.lambdify(self.x, function(), "numpy")

        for i in range(0, len(x_arr)):
            # calculate y for each given y
            y[i] = f(x_arr[i])

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