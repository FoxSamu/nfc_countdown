DEBUG = True
INFO = True
ERROR = True

def debug(str):
    if DEBUG:
        print("[DEBUG] " + str)

def info(str):
    if INFO:
        print("[INFO]  " + str)

def error(str):
    if ERROR:
        print("[ERROR] " + str)