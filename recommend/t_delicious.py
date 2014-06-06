import json
import cPickle as pickle
import traceback


Categories=('user','link','tag')
Dicx=dict(zip(Categories, ({},)*len(Categories)))
Sep=', '


def main(fi_name='delicious-rss-1250k'):
    fi=open(fi_name)
    fo=open('./%s.inx' %fi_name, 'wb')
    fo.write('#format: user_id, link_id, *tag_id\n')
    for l in fi:
        try:
            uname, link, tags =parse(l)
            un = indexing(uname, 'user')
            ln = indexing(link, 'link')
            tns = [indexing(t, 'tag') for t in tags]
            fo.write(Sep.join((un, ln, Sep.join(tns)))+'\n')
        except Exception, e:
            #print traceback.format_exc()
            pass
    fo.close()
    pickle.dump(Dicx, open('Dicx.pkl','wb'))


def parse(txt):
    o = json.loads(txt)
    uname, link = [o[i] for i in ('author','link')]
    assert 'tags' in o
    tags=[t['term'] for t in o['tags']]
    return uname, link, tags
    

def indexing(s, cat):
    assert cat in Dicx
    if s in Dicx[cat]:
        n = Dicx[cat][s]
    else:
        n = Dicx[cat][s]= len(Dicx[cat])
    return str(n)


if __name__=='__main__':
    main()
