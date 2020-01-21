import os


def create_folder(name, experiment_mode, device):
    try:
        os.makedirs("Results_backup"+str(experiment_mode)+"/")
    except OSError:
        pass

    try:
        os.makedirs(os.path.join("Results_backup"+str(experiment_mode)+"/" + name, device))
    except OSError:
        pass


def write_to_file(name, experiment_mode, device, order, function_id, x, y):
    if(name == ""):
        return

    filename = "Results_backup"+str(experiment_mode)+"/" + name + '/' + device + '/' + str(int(order[function_id])) + '_' + str(function_id) + '.txt'

    with open(
        filename,
        'a'
    ) as file:
        file.write(str(x) + ' ' + str(y) + '\n')


def delete_file(name, experiment_mode, device, order, function_id):
    filename = "Results_backup"+str(experiment_mode)+"/" + name + '/' + device + '/' + str(int(order[function_id])) + '_' + str(function_id) + '.txt'
    if os.path.exists(filename):
        os.remove(filename)
