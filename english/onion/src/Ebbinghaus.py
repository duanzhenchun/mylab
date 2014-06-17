#period = [60*i for i in (20, 60, 12*60, 24*60, 2*24*60, 5*24*60, 8*24*60)]
period = [60*60*24 * i for i in (1, 3, 7, 15, 30)]

def finished(n):
    return n >= len(period)-1

