import os.path
import json


def lib_installer():

    path = os.path.abspath("../_build")
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


def path_invoke():

    path = os.path.abspath("../_build")

    with open(os.path.join(path, 'UserAppInfo.json'), 'r') as f:
        return json.load(f)



