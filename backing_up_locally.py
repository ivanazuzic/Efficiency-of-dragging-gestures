import os


def create_folder(name, device):
    try:
        os.makedirs("Results_backup/")
    except OSError:
        pass

    try:
        os.makedirs(os.path.join("Results_backup/" + name, device))
    except OSError:
        pass


def write_to_file(name, device, order, x, y):
    filename = "Results_backup/" + name + '/' + device + '/' + str(order[function_id]) + '_' + '.txt'

    with open(
        filename,
        'a'
    ) as file:
        file.write(str(x) + ' ' + str(y) + '\n')


def delete_file(name, device, order, function_id):
    filename = "Results_backup/" + name + '/' + device + '/' + str(order[function_id]) + '_' + str(function_id) + '.txt'
    if os.path.exists(filename):
        os.remove(filename)
