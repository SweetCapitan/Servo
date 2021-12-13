from datetime import datetime


def get_time():
    iso = datetime.now().isoformat()
    return iso[11:19]


def log(text):
    print(f"\033[32m {get_time()} [Logs] \033[37m{str(text)}")


def warn(text):
    print(f"\033[33m\033[3m {get_time() + ' [Warning] ' + str(text)}")


def error(text):
    print(f"\033[31m\033[1m {get_time() + ' [Error] ' + str(text)}")


def comm(text):
    print(f"\033[32m {get_time()} [Logs][Command] \033[37m{str(text)}")
