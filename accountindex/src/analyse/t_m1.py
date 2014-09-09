import m1, m2

def monkeypatch_bitext(source, target):
    for (s, t) in zip(source, target):
        if s.strip() and t.strip():
            yield (s.strip().split(), t.strip().split())

m1.bitext = monkeypatch_bitext

S = '''a b 
b c
c
d d d d b
'''
T = '''B A
C B 
C
D A D D A B
'''
S, T = S.split('\n'), T.split('\n')

def tiny_test(model):
    model.iterate(1000, True)
    for k, v in model.t.iteritems():
        print '%s: %s = %.2f' % (k, max(v, key=v.get), max(v.values())) 
    for i in model.decode_training():
        print i
    return model.t
    
if __name__ == '__main__':
#     model = m1.M1(S, T)
    model = m2.M2(S, T)
    tiny_test(model)
