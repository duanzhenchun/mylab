period = [60*60*24 * i for i in (1.0/48, 1./3, 1, 3, 7, 15, 30)]

def finished(n):
    return n >= len(period)-1

