from curve_functions import *

fp = FunctionProvider()

for test in range(len(fp.function_array)):
    for difficulty in range(len(fp.function_array[test])):
        for task in range(len(fp.function_array[test][difficulty])):
            print(test, difficulty, task)
            analysis = fp.get_function_analysis(difficulty, task, np.linspace(0, 5, 1000), test)
            print(analysis)
