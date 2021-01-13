import json
from . import PathFinder as pf



def db_log_retriver():
    pf.lib_installer()
    log = pf.path_invoke()

    with open(log['DB_logger'], 'r') as p_json:
        return json.load(p_json)


def img_retrivre():

    pf.lib_installer()
    log = pf.path_invoke()
    return log['Img_dir']
