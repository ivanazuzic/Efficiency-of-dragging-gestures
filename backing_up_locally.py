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


def write_to_file(name, experiment_mode, device, function_order, projection_order, function_idx, x, y):
    if(name == ""):
        return

    filename = get_filename(name, experiment_mode, device, function_order, projection_order, function_idx)

    with open(
        filename,
        'a'
    ) as file:
        file.write(str(x) + ' ' + str(y) + '\n')


def delete_file(name, experiment_mode, device, function_order, projection_order, function_idx):
    filename = get_filename(name, experiment_mode, device, function_order, projection_order, function_idx)
    if os.path.exists(filename):
        os.remove(filename)

def get_filename(name, experiment_mode, device, function_order, projection_order, function_idx):
    return (
        "Results_backup"+str(experiment_mode)+"/" + name + '/' + device + 
        '/id-' + str(int(function_order[function_idx])) + 
        '_proj-' + str(int(projection_order[function_idx])) + 
        '_order-' + str(function_idx) + '.txt'
    )