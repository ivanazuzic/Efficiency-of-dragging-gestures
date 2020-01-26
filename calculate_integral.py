from curve_functions import *
import os
import json
import sympy as sp

fp = FunctionProvider()


def calculate_curvature_integral():
    for test in range(len(fp.function_array)):
        for difficulty in range(len(fp.function_array[test])):
            for task in range(len(fp.function_array[test][difficulty])):
                print(test, difficulty, task)
                analysis = fp.get_function_analysis(difficulty, task, np.linspace(0, 5, 1000), test)
                print(analysis)


x = sp.Symbol("x")

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


calculate_all_user_movement_integrals()
