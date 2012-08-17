#width traval contacts, use list, append
import sys
from data import *
import logging
from redisclient import *

commit_intervel=50
max_user=1000000
max_results={'max-results':100}        
        
def get_contacts(iD,db):
    dic=get_ret( person_fmt+str(iD)+'/'+CONTACTS, max_results)
    if not dic:
        return
    contacts=dic.pop('entry')
    Tos=[]
    for cont in contacts:
        p=Person(cont,db)
        pid=p.dic['id'] 
        Tos.append( pid[pid.rfind('/')+1:])
    return Tos        

def incr_count(dic, k):
    dic[k]=dic.setdefault(k,0)+1
        
import sys
from util import *   

def travel():
    init_log()
    
    traveling=map(str, randselect(40))
    logging.info('init traveling:%s' %traveling)
    
    db=dbmgr.dbmanager('douban.db')
    
    #init db table
    dic=get_ret(person_fmt+'62508021')
    assert dic
    Person(dic,db)
    
    visited=0
    while traveling or max_user < max_user:
        #progressbar(max_user,len(traveling))
        iD=traveling.pop(0)
        logging.info('traveling len:%d' %len(traveling))
        visited+=1
        Tos = get_contacts(iD,db)
        if not Tos:
            continue
        out_w=1.0/len(Tos)
        for j in Tos: 
            rdscli.sadd(CONTACTS + ':'+iD,j) #get them by smembers
            logging.debug('R_CONTACTS:%s %s'%(j,iD))
            rdscli.zadd(R_CONTACTS+':'+j,iD, out_w )
         
            if not rdscli.keys(CONTACTS + ':'+j): #not visited before
                traveling.append(j)
        if visited % commit_intervel == 0:
            db.commit()

def construct_r_contacts():
    for i in rdscli.keys(CONTACTS+'*'):
        From=i[i.find(':')+1:]
        Tos = rdscli.smembers(i)
        out_w = 1.0/len(Tos)
        for j in Tos: 
            rdscli.zadd(R_CONTACTS+':'+j, From, out_w )        
        
                    
def stat_hot():
    rdscli.delete(hotPeople)
    for i in rdscli.keys(R_CONTACTS+'*'):
        To=i[i.find(':')+1:]
        r_scores = rdscli.zrange(i,0,-1,withscores=True)
        hotv = 0
        for score in r_scores:
            hotv += score[1]
        rdscli.zadd(hotPeople,To,hotv)
    return rdscli.zrevrangebyscore(hotPeople, 
        sys.maxint,0, start=0, num=20, withscores=True)       

def similar(p1,p2):
    "return range: [0,1]"
    if p1 == p2:
        print 'same person'
        return 0
    Tos1,Tos2 = [getTos(p) for p in (p1,p2)]
    if not Tos1 or not Tos2:
        logging.info('no Tos')
        return 0
    common=[]
    for To in Tos1:
        if To in Tos2:
            common.append(To)
    if common:
        print 'common contacts:', common
    return len(common)**2 * 1.0 /len(Tos1)/len(Tos2)

def find_circle(pid):
    assert pid
    traveling=[pid]
    for i in xrange(1000):
        if not traveling:
            break
        From = traveling.pop(0)
        Tos=getTos(From)
        if not Tos:
            continue
        for To in Tos:
            if To == pid:   
                print 'got %s  after:%d travel' %(pid,i)
                return
            if not To in traveling:
                traveling.append(To)    

def find_pair(From):
    "concern each other"
    Tos=getTos(From)
    if not Tos:
        return
    for To in Tos:
        if To == From:   
            print '%s and %s are pair' %(From,i)
            return    
      
def t_pair():
    for i in xrange(2000):
        find_pair(randFrom())
            
def googlemap():
    pass
        
def t_similar():
    for i in range(200):
        p1,p2 = randFrom(),randFrom()
        res = similar(p1,p2)
        if res>0: 
            print 'after:', i, p1,p2,res   
        
def test():
#    construct_r_contacts()
#    print stat_hot()
#    find_circle(randFrom())
    t_pair()
#    t_similar()    
    
#test()
travel()
