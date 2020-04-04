from curve_functions import *
import os
import json
import sympy as sp
import numpy as np

fp = FunctionProvider()
x = sp.Symbol("x")


def calculate_curvature_integral():
    integrals_approx = {}
    for test in range(len(fp.function_array)):
        integrals_approx[test] = {}
        for difficulty in range(len(fp.function_array[test])):
            tasks_num = len(fp.function_array[test][difficulty])
            for task in range(tasks_num):
                function_id = tasks_num * difficulty + task
                print("########## Test mode:", test, "; Difficlty:", difficulty, "; Task:", task)
                kappa = fp.get_function_curvature(difficulty, task, test)
                print(kappa)
                kappa = sp.lambdify(x, kappa, "numpy")

                # because of the complex calculation revolving the curvature
                # (kappa), we instead calculate its approximation
                # by summing up y values for each x0 in such a way that
                # the distance between two x0 points is infinitely small
                integral_approx = 0
                x0 = 0.00  # begin point
                x1 = 5.00  # end point
                # number of points we want to sum up (must be very big)
                numpoints = (x1 - x0) * 100000.00
                # distance between two points (will be very small)
                delta = (x1 - x0) / numpoints
                i = 0
                while x0 < x1:
                    # put integral_approx calculation inside try-except
                    # in case we get "division by zero" exception.
                    if(i % (numpoints / 10) == 0):
                        # this condition is meant to represent a "loading bar"
                        # it will print the current percentage of points processed
                        print(round(x0 / x1, 3) * 100, "%  done")
                    try:
                        integral_approx += kappa(x0)
                    except Exception as e:
                        # this might, on very rare occassions, be
                        # "division by zero"
                        print(e)
                    finally:
                        x0 += delta
                        i += 1

                print("Integral: ", integral_approx, "\n")
                integrals_approx[test][str(function_id)] = str(integral_approx)

    file = open("curvature_integrals.json", "w")
    file.write(json.dumps(integrals_approx, sort_keys=True, indent=4))
    file.close()


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
            # this dictionary's keys will are function_id's
            function_id = (tasks[task][0])
            result[function_id] = []

        for task in range(len(tasks)):
            function_id = str(tasks[task][0])

            # for each task, get all the coordinates our user drew
            data = open(foldername + "/" + tasks[task], "r")
            coordinates = data.readlines()

            integral = 0
            for i in range(1, len(coordinates)):
                coordinate1 = coordinates[i - 1].split()
                coordinate2 = coordinates[i].split()
                x1 = float(coordinate1[0])  # x coordinate of first point
                y1 = float(coordinate1[1])
                x2 = float(coordinate2[0])  # x coordinate of second point
                y2 = float(coordinate2[1])

                # if values have the same x, just continue
                if(x2 == x1):
                    continue

                # get the equation of the line on which point1 and point2 lay
                f = (y2 - y1) / (x2 - x1) * (x - x1) + y1
                # calculate integral of surface where f is the upper bound
                # and -2.5 is lower_bound
                tmp = sp.integrate(f - (-2.5), (x, x1, x2))
                integral += tmp

            # append this integral to the array at result[function_id]
            # turn the float into string so it can be serialized into JSON
            result[function_id].append(str(integral))
            data.close()

    except Exception as e:
        print(e)
        raise

    return result


def calculate_all_user_movement_integrals():
    experiment_mode = [0, 1]
    path = "Results_backup"
    file = open("movement_integrals.json", "w")

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

calculate_curvature_integral()