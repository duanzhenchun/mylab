import redis


K_freq = 'onion_en_freq'
K_uk = 'onion_en_uk'
K_K = 'onion_en_K' 
K_IPA = 'onion_en_IPA'

K_known = 'onion_en_known:%d' 
K_unknown ='onion_en_unknown:%d' 
K_forget='onion_en_forget:%d' 
K_tl = 'onion_en_tl:%d'
K_curpage = 'onion_en_curpage:%d'
K_cache = 'onion_en_cache:%d'

Word0 = 'pointedly'
Uid0 = 4

Limit_memo = 1000
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

