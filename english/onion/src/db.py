import redis


K_K = 'onion_en_K:%d' 
K_known = 'onion_en_known:%d' 
K_unknown ='onion_en_unknown:%d' 
K_tl = 'onion_en_tl:%d'

K_freq = 'onion_en_freq'
K_uk = 'onion_en_uk'

K_IPA = 'onion_en_IPA'

K_uid = 'onion_en_uid:'
K_nextuid = 'onion_en_next_user_id'

Word0 = 'freak'
Uid0 = 4

Mem =redis.Redis()
