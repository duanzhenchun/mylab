import redis


K_freq = 'onion_en_freq'
K_uk = 'onion_en_uk'
K_K = 'onion_en_K' 
K_IPA = 'onion_en_IPA'
K_encs = 'onion_en_cs'

K_known = 'onion_en_known:%d' 
K_unknown ='onion_en_unknown:%d' 
K_forget='onion_en_forget:%d' 
K_tl = 'onion_en_tl:%d'
K_curpage = 'onion_en_curpage:%d'
K_cache = 'onion_en_cache:%d'

Word0 = 'pointedly'
Uid0 = 4

Limit_memo = 5000
Limit_forget = 100

Mem =redis.Redis(db=1)

def movedb():
    db=redis.Redis(db=0)
    for key in (K_freq, K_uk, K_K, K_IPA):
        db.move(key, 1)
    for k in (1,4,5,8):
        for key in (K_known, K_unknown, K_forget, K_tl, K_curpage, K_cache):
            db.move(key %k, 1)
    db1= redis.Redis(db=1)
    db1.save()


def backup(uid):
    dic={}
    for k in (K_known, K_unknown, K_forget, K_curpage, K_cache):
        dic[k] = Mem.hgetall(k %uid)
    dic[K_tl] = Mem.zrange(K_tl %uid, 0, 10**5, withscores=True)
    return dic

def update(uid):
    for k in (K_known, K_unknown, K_forget, K_curpage, K_cache):
        for k1,v1 in dic[k].iteritems():
            Mem.hset(k %uid, k1,v1)
    for (k,v) in dic[K_tl]:
        Mem.zadd(K_tl %uid, k,v)


def detect_int():
    dici={}
    for w in Mem.hkeys(K_encs):
        if Mem.hget(K_encs,w).isdigit():
            dici[w]=v

def stats():
    k=K_cache.split('%')[0]+'*'
    uids = set([i.split(':')[1] for i in Mem.keys(k)])
    uids.update(set(Mem.hkeys(K_K)))
    print "#format:\nuid, #file, #timeline, (K_K, n/10)"
    for uid in uids:
        uid=int(uid)
        print uid, Mem.hlen(K_curpage %uid), Mem.zcard(K_tl %uid), Mem.hget(K_K, uid)


if __name__=="__main__":
    stats()
