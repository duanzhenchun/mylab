import redis


K_freq = 'onion_en_freq'
K_uk = 'onion_en_uk'
K_IPA = 'onion_en_IPA'

K_K = 'onion_en_K' 
K_known = 'onion_en_known:%d' 
K_unknown ='onion_en_unknown:%d' 
K_forget='onion_en_forget:%d' 
K_tl = 'onion_en_tl:%d'
K_curpage = 'onion_en_curpage:%d'
K_cache = 'onion_en_cache:%d'

Word0 = 'pointedly'
Uid0 = 4

Mem =redis.Redis()
