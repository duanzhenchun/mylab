#width traval contacts, use list, append
import sys
from data import *
import logging

hotPeople = 'douban:hotpeople'
CONTACTS = 'contacts'
R_CONTACTS = 'rev_contacts'

commit_intervel=50
max_user=1000000
max_results={'max-results':100}        
        
def get_contacts(iD,db,rdscli):
    dic=get_ret( person_fmt+str(iD)+'/'+CONTACTS, max_results)
    if not dic:
        return
    contacts=dic.pop('entry')
    Tos=[]
    for cont in contacts:
        p=Person(cont,db,rdscli)
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
    logging.info(traveling)
    
    db=dbmgr.dbmanager('douban.db')
    rdscli=redis.client.Redis()
    
    #init db table
    dic=get_ret(person_fmt+'62508021')
    assert dic
    Person(dic,db,rdscli)
    
    visited=0
    while traveling or max_user < max_user:
        #progressbar(max_user,len(traveling))
        iD=traveling.pop(0)
        logging.debug('traveling len:', len(traveling))
        visited+=1
        Tos = get_contacts(iD,db,rdscli)
        if not Tos:
            continue
        out_w=1.0/len(Tos)
        for j in Tos: 
            rdscli.sadd(CONTACTS + ':'+iD,j) #get them by smembers
            logging.debug('R_CONTACTS', j, iD)
            rdscli.zadd(R_CONTACTS+':'+j,iD, out_w )
         
            if not rdscli.keys(CONTACTS + ':'+j): #not visited before
                traveling.append(j)
        if visited % commit_intervel == 0:
            db.commit()

def construct_r_contacts(rdscli):
    for i in rdscli.keys(CONTACTS+'*'):
        From=i[i.find(':')+1:]
        Tos = rdscli.smembers(i)
        out_w = 1.0/len(Tos)
        for j in Tos: 
            rdscli.zadd(R_CONTACTS+':'+j, From, out_w )        
        
                    
def calc_hot(rdscli):
    for i in rdscli.keys(R_CONTACTS+'*'):
        To=i[i.find(':')+1:]
        r_scores = rdscli.zrange(i,0,-1,withscores=True)
        hotv = 0
        for score in r_scores:
            hotv += score[1]
        rdscli.zadd(hotPeople,To,hotv)
    print rdscli.zrevrangebyscore(hotPeople, 
        sys.maxint,0, start=0, num=20, withscores=True)       

def test():
    rdscli=redis.client.Redis()
#    construct_r_contacts(rdscli)
    calc_hot(rdscli)


def TODO():
    pass
"""
concern each other
map distribution, maybe google map api
"""

def ringlen(rdscli,pid):
    traveling=[pid]
    while True:
        Tos=getTos(rdscli,traveling.pop(0))
        if To in traveling:
            continue
        for To in Tos:
            if To == pid:   
                print 'got it', To
                break
            if not To in traveling:
                traveling.append(To)    
                rdscli.zadd(R_CONTACTS+':'+j, From, out_w )        

def getTos(rdscli,pid):
    From = CONTACTS+':'+pid
    return rdscli.smembers(From)

def similar(p1,p2):
    "return range: [0,1]"
    rdscli=redis.client.Redis()
    Tos1,Tos2 = [getTos(rdscli,p) for p in (p1,p2)]
    if not Tos1 or not Tos2:
        return 0
    count=0
    for To in Tos1:
        if To in Tos2:
           count +=1
    return count**2/len(Tos1)/len(Tos2)

def t_similar():
    print similar('2005040','50473758')

#t_similar()
travel()
