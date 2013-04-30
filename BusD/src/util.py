import time

def now_str():
    return time.strftime('%Y-%m-%d %H:%M:%S %Z')

def now_int():
    return int(time.time())