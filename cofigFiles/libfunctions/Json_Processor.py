import json
import os.path

"""
def lib_installer():

    path = os.path.abspath("../.build")
    write_path = path
    img_path = os.path.abspath('../icons')

    done = False
    if done is False:
        try:

            with open(os.path.join(path, 'UserAppInfo.json'), 'r') as f:
                p_json = json.load(f)

            if p_json['install'] == '1':
                done = True
                return True

        except FileNotFoundError:

            path = os.path.join(path, 'DataBaseAccessDB.json')

            dados = {

                'install': '1',
                'DB_logger': path,
                'Img_dir': img_path

            }
            with open(os.path.join(write_path, "UserAppInfo.json"), 'w') as file:
                json.dump(dados, file, indent=4)

"""
def path_invoke():

    path = ".. .build"

    with open(os.path.join(path, 'UserAppInfo.json'), 'r') as f:
        return json.load(f)


def db_log_retriver():
    #lib_installer()
    log = path_invoke()

    with open(log['DB_logger'], 'r') as p_json:
        return json.load(p_json)

"""
def img_retrivre():

    lib_installer()
    log = path_invoke()
    return log['Img_dir']
"""