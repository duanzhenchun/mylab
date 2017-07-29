import redis

hotPeople = 'douban:hotpeople'
CONTACTS = 'contacts'
R_CONTACTS = 'rev_contacts'


rdscli=redis.client.Redis()

def getTos(pid):
    From = CONTACTS+':'+pid
    return rdscli.smembers(From)

def randkey(pre, count=100):
    while count:
        k=rdscli.randomkey()
        if k.startswith(pre):
            return k
    return None

def randFrom():
    From = randkey(CONTACTS)
    if From:
        From = From[From.find(':')+1:]
    return From
