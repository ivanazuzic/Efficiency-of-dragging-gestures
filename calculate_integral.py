from curve_functions import *
import os
import json
import sympy as sp
import numpy as np
import math

fp = FunctionProvider()
x = sp.Symbol("x")
epsilon = 0.000001

def calculate_curvature_integral():
    integrals_approx = {}
    for test in range(len(fp.function_array)):
        integrals_approx[test] = {}
        for difficulty in range(len(fp.function_array[test])):
            tasks_num = len(fp.function_array[test][difficulty])
            for task in range(tasks_num):
                function_id = tasks_num * difficulty + task
                print("########## Test mode:", test + 1, "; Difficlty:", difficulty + 1, "; Task:", task + 1)
                kappa = fp.get_function_curvature(difficulty, task, test)
                # print("Sympy intergation:", sp.integrate(kappa,x), sp.integrate(kappa, (x, 0, math.pi / 3)), "\n")
                # because of the complex calculation revolving the curvature
                # (kappa), we instead calculate its approximation
                # by summing up y values for each x0 in such a way that
                # the distance between two x0 points is infinitely small

                x0 = 0
                x1 = 2 * math.pi

                print(kappa)
                kappa = sp.lambdify(x, kappa, "numpy")

                integral_approx = calculate_riemann_integral(kappa, x0, x1, 1000)
                print("Integral: ", integral_approx, "\n")
                integrals_approx[test][str(function_id)] = str(integral_approx)

    file = open("analysis/curvature_integrals.json", "w")
    file.write(json.dumps(integrals_approx, sort_keys=True, indent=4))
    file.close()


def calculate_riemann_integral(f, x0, x1, numpoints):
    integral_approx = 0
    # distance between two points (will be very small)
    delta = (x1 - x0) / numpoints
    i = 0
    for i in range(numpoints):
        # put integral_approx calculation inside try-except
        # in case we get "division by zero" exception.
        if(i % (numpoints / 10) == 0):
            # this condition is meant to represent a "loading bar"
            # it will print the current percentage of points processed
            # print(round(x0 / x1, 3) * 100, "%  done")
            pass
        try:
            # Riemann sum
            integral_approx += abs(f(x0) * delta)
        except Exception as e:
            # this might, on very rare occassions, be
            # "division by zero"
            print(e)
        finally:
            x0 += delta
            i += 1
    return integral_approx


def calculate_user_movement_integral(user, experiment_mode=0, device="Mouse"):
    foldername = (
        "Results_backup" +
        str(experiment_mode) +
        "/" + user +
        "/" + device
    )

    result = {}
    try:
        # get all tasks our user performed
        tasks = sorted(os.listdir(foldername))
        for task in range(len(tasks)):
            # this will produce a dictionary with all values being empty lists.
            # this dictionary's keys are function_id's
            function_id = (tasks[task][3])
            result[function_id] = {}
        
        for task in range(len(tasks)):
            # add projection to dictionary
            projection = int(tasks[task][10])
            function_id = (tasks[task][3])
            result[function_id][projection] = {'integral': [], 'error': []}

        for task in range(len(tasks)):
            projection = int(tasks[task][10])
            function_id = str(tasks[task][3])

            # for each task, get all the coordinates our user drew
            data = open(foldername + "/" + tasks[task], "r")
            coordinates = data.readlines()
            print(tasks[task], " ---> is being processed, coordinate number:", len(coordinates))

            integral = 0
            # at each segment, subtract surfaces of the real function and user movement
            error_integral = 0
    
            difficulty = int(int(function_id) / 2)
            test = int(function_id) % 2
            real_func = fp.provide_function(difficulty, test, projection)
            real_func = 0.5 * real_func ** 2
            real_func = sp.lambdify(x, real_func)

            for i in range(1, len(coordinates)):
                coordinate1 = coordinates[i - 1].split()
                coordinate2 = coordinates[i].split()
                x1 = float(coordinate1[0])  # x coordinate of first point
                y1 = float(coordinate1[1])
                x2 = float(coordinate2[0])  # x coordinate of second point
                y2 = float(coordinate2[1])

                tmp_x1, tmp_y1 = x1, y1
                tmp_x2, tmp_y2 = x2, y2

                if(is_cartesian(projection) is False):
                    if(abs(x1 - x2) > 2 * math.pi - 1):
                        # what if points are at 2pi - 0 interval (crossing)
                        if(x1 > x2):
                            x1 = x1 - 2 * math.pi
                            tmp_x1 = x1
                        else:
                            x2 = x2 - 2 * math.pi
                            tmp_x2 = x2

                    x1, y1 = (y1 * np.cos(x1), y1 * np.sin(x1))
                    x2, y2 = (y2 * np.cos(x2), y2 * np.sin(x2))

                if(abs(x2 - x1) < epsilon):
                    continue

                # get the equation of the line on which point1 and point2 lay
                k = 0
                try:
                    k = (y2 - y1) / (x2 - x1)
                except:
                    continue

                f = k * (x - x1) + y1
                if(is_cartesian(projection) is False):
                    f = sp.lambdify(x, f, "numpy")
                    f = f(0) / (sp.sin(x) - (f(1) - f(0)) * sp.cos(x))
                    f = 0.5 * f**2

                    # restore cartesian coordinates back to polar
                    x1, y1 = tmp_x1, tmp_y1
                    x2, y2 = tmp_x2, tmp_y2

                f = sp.lambdify(x, f, "numpy")

                # calculate integral of user plotted line
                tmp = calculate_riemann_integral(f, x1, x2, 100)
                # calculate integral of the real function at the same segment
                tmp2 = calculate_riemann_integral(real_func, x1, x2, 100)
                error_integral += abs(tmp - tmp2)

                # if(tmp > 1):
                #     print(i, ": Integral: ", tmp, ' :: (', tmp_x1, ',', tmp_y1, ',   ', tmp_x2,',', tmp_y2, ")")
                integral += tmp

            # append this integral to the array at result[function_id]
            # turn the float into string so it can be serialized into JSON
            # print(tasks[task], " result: ", integral, "error:", error_integral)
            # print("Actual surface", calculate_riemann_integral(real_func, 0, 2 * math.pi, 100)) 

            result[function_id][projection]["integral"].append(str(integral))
            result[function_id][projection]["error"].append(str(error_integral))
            data.close()

    except Exception as e:
        print(e)
        raise

    return result


def calculate_all_user_movement_integrals():
    experiment_mode = [0, 1]
    path = "Results_backup"
    file = open("analysis/movement_integrals.json", "w")

    results_arr = {}

    for test in experiment_mode:
        # for each test
        userdir = os.listdir(path + str(test))
        results_arr[test] = {}
        for user in userdir:
            print(user)
            # for each user
            results_arr[test][user] = {}
            devicedir = os.listdir(path + str(test) + "/" + user)
            for device in devicedir:
                # get all devices
                # calculate the user's movement integral on this device.
                result = calculate_user_movement_integral(user, test, device)
                results_arr[test][user][device] = result

    file.write(json.dumps(results_arr, sort_keys=True, indent=4))
    file.close()


# uncomment this to calculate integral of all user movements
# calculate_all_user_movement_integrals()

calculate_user_movement_integral("galebftw", 0)
# calculate_curvature_integral()
