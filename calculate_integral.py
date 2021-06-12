from curve_functions import *
import os
import json
import sympy as sp
import numpy as np
import math
import display_properties
import pandas as pd

fp = FunctionProvider()
x = sp.Symbol("x")
epsilon = 0.000001
PROJECTIONS = ['Cartesian', 'Polar']
FUNC_IDS = [0, 1, 2, 3, 4, 5]
DEVICES = ['Mouse', 'Graphic tablet']
TEST_MODES = [0, 1]


x0 = 0
x1 = 2 * math.pi
N = 10000

def calculate_index_of_difficulty_integral():
    integrals_approx = {}
    for test in range(len(fp.function_array)):
        integrals_approx[test] = {}
        for difficulty in range(len(fp.function_array[test])):
            tasks_num = len(fp.function_array[test][difficulty])
            for task in range(tasks_num):
                function_id = tasks_num * difficulty + task
                print("########## Test mode:", test + 1, "; Difficlty:", difficulty + 1, "; Task:", task + 1)
                kappa = fp.get_function_curvature(difficulty, task, test)
                length = fp.get_function_length(difficulty, task, test)

                # print("Sympy intergation:", sp.integrate(kappa,x), sp.integrate(kappa, (x, 0, math.pi / 3)), "\n")
                # because of the complex calculation revolving the curvature
                # (kappa), we instead calculate its approximation
                # by summing up y values for each x0 in such a way that
                # the distance between two x0 points is infinitely small

                # alpha = maximum error the user was allowed (maximum dist between drawn y and real y)
                alpha = 1 # 0.9678520380625855

                if(is_cartesian(test)):
                    length = length * display_properties.CARTESIAN_UNIT_LENGTH_IN_INCH
                    alpha *= display_properties.CARTESIAN_UNIT_LENGTH_IN_INCH
                else:
                    length = length * display_properties.POLAR_UNIT_LENGTH_IN_INCH
                    alpha *= display_properties.POLAR_UNIT_LENGTH_IN_INCH

                length = sp.lambdify(x, length, "numpy")
                length = calculate_riemann_integral(length, x0, x1, N)

                kappa = sp.lambdify(x, kappa, "numpy")
                kappa = calculate_riemann_integral(kappa, x0, x1, N)

                # index_of_difficulty = sp.log((length + kappa) + 1, 2)
                # index_of_difficulty = kappa
                # index_of_difficulty = length
                # index_of_difficulty = sp.log(kappa * display_properties.LINEWIDTH_IN_INCH / length + 1, 2)
                # index_of_difficulty = length / display_properties.LINEWIDTH_IN_INCH + kappa
                index_of_difficulty = np.log2(length / alpha + kappa + 1)
                # index_of_difficulty = alpha  # alpha is 'w'
                print(index_of_difficulty)
                integral_approx = index_of_difficulty

                print("Integral: ", integral_approx, "\n")
                integrals_approx[test][str(function_id)] = str(integral_approx)

    # file = open("analysis/index_of_difficulty-log(kappa+length).json", "w")
    # file = open("analysis/index_of_difficulty-kappa.json", "w")
    # file = open("analysis/index_of_difficulty-length.json", "w")
    # file = open("analysis/index_of_difficulty-log(kappa*w:length+1).json", "w")
    # file = open("analysis/index_of_difficulty-length:w+kappa.json", "w")
    file = open("analysis/index_of_difficulty-log(length:alpha+kappa+1).json", "w")
    # file = open("analysis/index_of_difficulty-w.json", "w")
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
    return integral_approx


def calculate_user_movement_integral(user, experiment_mode=0, device="Mouse"):
    foldername = (
        "Results_backup" +
        str(experiment_mode) +
        "/" + user +
        "/" + device
    )

    result = {}

    all_errors = []
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
            data.close()
            # print(tasks[task], " ---> is being processed, coordinate number:", len(coordinates))

            integral = 0
            # at each segment, subtract surfaces of the real function and user movement
            error_integral = 0

            difficulty = int(int(function_id) / 2)
            test = int(function_id) % 2
            real_func = fp.provide_function(difficulty, test, projection)
            # real_func = 0.5 * real_func ** 2
            real_func = sp.lambdify(x, real_func)


            for i in range(1, len(coordinates)):
                coordinate1 = coordinates[i - 1].split()
                coordinate2 = coordinates[i].split()
                x1 = float(coordinate1[0])  # x coordinate of first point
                y1 = float(coordinate1[1])
                x2 = float(coordinate2[0])  # x coordinate of second point
                y2 = float(coordinate2[1])
                
                real_y1 = real_func(x1)
                real_y2 = real_func(x2)
                all_errors.append(y1-real_y1)
                all_errors.append(y2-real_y2)
                
                # if(is_cartesian(projection) is False):
                #     if(abs(x1 - x2) > 2 * math.pi - 2):
                #         # what if points are at 2pi - 0 interval (crossing)
                #         if(x1 > x2):
                #             x1 = x1 - 2 * math.pi
                #         else:
                #             x2 = x2 - 2 * math.pi

                # if(abs(x2 - x1) < epsilon):
                #     continue

                # get the equation of the line on which point1 and point2 lay
                # k = 0
                # try:
                #     k = (y2 - y1) / (x2 - x1)
                # except:
                #     continue

                # f = k * (x - x1) + y1
                # if(is_cartesian(projection) is False):
                #     # f = sp.lambdify(x, f, "numpy")
                #     # f = f(0) / (sp.sin(x) - (f(1) - f(0)) * sp.cos(x))
                #     f = (y1 + y2) / 2
                #     f = 0.5 * f**2

                # f = sp.lambdify(x, f, "numpy")

                # # calculate integral of user plotted line
                # tmp = calculate_riemann_integral(f, x1, x2, 100)
                # # calculate integral of the real function at the same segment
                # tmp2 = calculate_riemann_integral(real_func, x1, x2, 100)
                # error_integral += abs(tmp - tmp2)

                # if(tmp > 1):
                #     print(i, ": Integral: ", tmp, ' :: (', tmp_x1, ',', tmp_y1, ',   ', tmp_x2,',', tmp_y2, ")")
                # integral += tmp

            # append this integral to the array at result[function_id]
            # turn the float into string so it can be serialized into JSON
            # print(tasks[task], " result: ", integral, "error:", error_integral)
            # print("Actual surface", calculate_riemann_integral(real_func, 0, 2 * math.pi, 100))

            # result[function_id][projection]["integral"].append(str(integral))
            # result[function_id][projection]["error"].append(str(error_integral))

    except Exception as e:
        print(e)
        raise


    print(np.max(all_errors))
    result['max'] = np.max(all_errors)
    return result


def calculate_all_user_movement_integrals():
    experiment_mode = [0, 1]
    path = "Results_backup"
    file = open("analysis/movement_integrals.json", "w")

    results_arr = {}

    all_errors = []

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
                all_errors.append(result["max"])
                results_arr[test][user][device] = result

    file.write(json.dumps(results_arr, sort_keys=True, indent=4))
    file.close()
    all_errors = sorted(all_errors, reverse=True)
    print("max errors", all_errors[:10])


def calculate_throughput():
    df = pd.read_csv('analysis/logs.csv')
    sortedParticipants = sorted(list(set(df['Participant name'])))
    lengthIoDsFile = open('analysis/index_of_difficulty-' + 'length' +'.json')
    lengthIoDs = json.load(lengthIoDsFile)
    lengthIoDsFile.close()
    kappaIoDsFile = open('analysis/index_of_difficulty-' + 'kappa' +'.json')
    kappaIoDs = json.load(kappaIoDsFile)
    kappaIoDsFile.close()

    separator = ";"
    ## NOTE::: look in calculate_integrals.y
    # this throughput calculation is not exactly correct :)
    for i in range(len(sortedParticipants)):
        participant = sortedParticipants[i]
        # print(participant, end='')
        # this will have two values; one for each device
        TPsForThisParticipant = {}
        
        for device in DEVICES:
            # the average throughput for this participant and this device
            # each user produces two throughputs: one for each device
            TPsForThisDevice = []
            for experimentMode in TEST_MODES:
                filename = "Results_backup%s/%s/%s" %(experimentMode, participant, device)
                files = os.listdir(filename)
                for file in files:
                    funcId = int(file[3])
                    projtmp = file[10]
                    projection = "Cartesian"
                    if(projtmp in ["2", "3"]):
                        projection = "Polar"
                    # we are searching for an entry in the logs which can tell us
                    # the average MT for user
                    # and the st dev of error rate for user.
                    # from the stdev of error rate, we will caluclate effective width of target (W_e)
                    # and from that we'll get effective index of difficulty - ID_e
                    # when we divide ID_e by the MT of the user, we get the user's throughput for a single curve
                    # and then we find the mean of all throughputs for this user, which we
                    # then use for t-test to compare the two pointing devices
                        
                    # filter out by projection, Cartesian or Polar
                    participantMovement = df[df['Function projection'] == projection]
                    # filter out by function ID
                    participantMovement = participantMovement[participantMovement['Function ID'] == funcId]
                    # filter out by test (experiment mode)
                    participantMovement = participantMovement[participantMovement['Test mode'] == experimentMode]
                    participantMovement = participantMovement[participantMovement['Participant name'] == participant]
                    # filter out by device
                    participantMovement = participantMovement[participantMovement['Device'] == device]
                    f = open(filename + "/" + file)
                    
                    # find the stdev of the error by dividing the sum of errors with the square root of
                    # the number of points (this is the stdev formula)
                    pointsDrawn = [pointDrawn.replace('\n', '') for pointDrawn in f.readlines()]
                    f.close()
                    numOfPointsDrawn = len(pointsDrawn)

                    test = int(projtmp)        
                    difficulty = int(int(funcId) / 2)
                    task = int(funcId) % 2
                    real_func = fp.provide_function(difficulty, task, test)
                    real_func = sp.lambdify(x, real_func)

                    # ALL of the error the user had made on this specific curve
                    allErrorVals = []

                    for pointDrawn in pointsDrawn:
                        x_coord = float(pointDrawn.split()[0])
                        y_coord = float(pointDrawn.split()[1])
                        real_y = real_func(x_coord)

                        y_diff = abs(y_coord - real_y)
                        
                        if(projtmp in ["2", "3"]):
                            # polar projection, erroval should be multiplied with the polar unit length
                            # so that we get effective width in inches
                            y_diff *= display_properties.POLAR_UNIT_LENGTH_IN_INCH
                        else:
                            y_diff *= display_properties.CARTESIAN_UNIT_LENGTH_IN_INCH

                        allErrorVals.append(y_diff)
                    # print(np.mean(allErrorVals), np.std(allErrorVals))
                    errorVal = np.std(allErrorVals)
                    
                    # this is from the effective target width (Fitts law), a true-tried-tested formula
                    W_e = 4.133 * errorVal
                    
                    # calculate effective ID_e for this W_e
                    kappa = float(kappaIoDs[str(test)][str(funcId)])
                    length = float(lengthIoDs[str(test)][str(funcId)]) 

                    Id_e = np.log2(length / W_e + kappa + 1)
                    
                    # movement time
                    MT = np.mean(participantMovement["Drawing time"].values)
                    
                    # throughput for this curve and this specific user
                    TP = Id_e / MT
                    TPsForThisDevice.append(TP)
                    # print(kappa, length,  W_e, MT, TP, file)
                    
                    # print(participant, projection, "(%s)" %projtmp, experimentMode, funcId, device, errorVal)
            # this is where the loop for each device ends --> we have to calculate
            # the avg throughput for this participant and this device
            TPsForThisParticipant[device] = np.mean(TPsForThisDevice)
        print(participant, TPsForThisParticipant["Mouse"], TPsForThisParticipant["Graphic tablet"], sep=separator)


# uncomment this to calculate integral of all user movements
# calculate_all_user_movement_integrals()

# calculate_user_movement_integral("galebftw", 0)
# calculate_index_of_difficulty_integral()

calculate_throughput()

#1.9836813461621188, 1.4294538125712348, 1.0630777427721778, 0.9678520380625855, 0.824185782388446, 0.788284265135631, 0.7865531957073231, 0.7783081287682021, 0.7459006389300387, 0.7440944953583698]
