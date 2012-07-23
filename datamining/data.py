
from redisclient import rdscli

from util import get_ret

person_fmt='http://api.douban.com/people/'
book_fmt='http://api.douban.com/book/subject/'
movie_fmt='http://api.douban.com/movie/subject/'

txt='$t'
link='link'
rel='@rel'
href='@href'
name='@name'
db_tag='db:tag'
count='@count'
author='author'
db_attr='db:attribute'
gd_rating='gd:rating'


class Person(object):
    Keys=[] #class property
    
    def __init__(self,dic,db):
        self.dic={}
        self.tags={}
        for k,v in dic.iteritems():
            dic[k]=v
        self._parse(dic)
        self.modify_key()
        if not self.__class__.Keys:
            self.createtable(db)
        self.save(db,False)
            
    def modify_key(self):
        moddic={}
        for k,v in self.dic.iteritems():
            moddic[k.replace(':','_').replace('-','_')]=v
        self.dic=moddic    
        
    def show(self):
        for k,v in sorted(self.dic.iteritems()):
            print k,v
                
    def tbl_fmt(self):       
        fmts=''
        for k,v in sorted(self.dic.iteritems()):
            fmts +=k
            if k=='id':
                fmts +=' unique'
            if type(v) == int:
                fmts +=' integer'
            fmts+=','
        fmts=fmts.rstrip(',') 
        tblname=self.__class__.__name__  
        tbl_fmt='%s(%s)' %(tblname,fmts)
        return tbl_fmt   
         
    def v_lst(self):
        vlst=[]
        for k in self.__class__.Keys:
            if not k in self.dic:
                v=''
            else:
                v=self.dic[k]    
                if type(v)==int:
                    v=str(v)
            vlst.append(v)
        return vlst
    
    def createtable(self,db):
        self.__class__.Keys=sorted(self.dic.keys())
        db.createtable(self.tbl_fmt()) 
            
    def save(self,db,cmt=True):
        db.save(self.__class__.__name__,self.v_lst(),cmt) 
        for k,v in self.tags.iteritems():
            rdscli.zadd(self.dic['id']+':'+db_tag,k,v) 
  
    def load(self,db):
        lst = db.load(self.__class__.__name__,self.dic['id'])
        vlst=[self.dic[k] for k in self.__class__.Keys if k in self.dic]
        #assert vlst == list(lst)
        res = rdscli.zrange(self.dic['id']+':'+db_tag,0,100)
                           
    def _parse(self,dic):
        for k,v in dic.iteritems():
            if txt in v:
                self.dic[k]=v[txt]
        if link in dic:
            for i in dic[link]:
                self.dic['%s_%s' %(link,i[rel])] = i[href]
        if db_attr in dic:
            for i in dic[db_attr]:
                self.dic['%s_%s' %(db_attr,i[name])] = i[txt]
    
class Book(Person):
    Keys=[]
    def _parse(self,dic):
        super(Book, self)._parse(dic)
        if author in dic:
            for i in dic[author]:
                self.dic[author] = i['name'][txt]          
        if db_tag in dic:
            for i in dic[db_tag]:
                self.tags[i[name]] = int(i[count])
        if gd_rating in dic:
            self.rating={}
            for k,v in dic[gd_rating].iteritems():
                self.rating[k] = str(v)
                
    def save(self,db,cmt=True):
        super(Book,self).save(db,cmt)
        rdscli.hmset(self.dic['id']+':'+gd_rating, self.rating)               
        
    def load(self,db):
        super(Book,self).load(db)
        dic = rdscli.hgetall(self.dic['id']+':'+gd_rating)
        assert self.rating == dic
        
class Movie(Book):
    Keys=[]
 
import dbmgr

def t_objs(cls,url_fmt,lst):
    db=dbmgr.dbmanager('douban.db')
    objs=[]
    for i in lst:
        dic=get_ret(url_fmt+str(i))
        if not dic:
            continue
        obj=cls(dic,db)
        objs.append(obj)
    else:
        db.commit()
        rdscli.save()
    #show
    for obj in objs:
        obj.load(db)    
        
def t_persons():
    lst=('6829400','antonia','yelucaizi','62508021',)    
    t_objs(Person,person_fmt,lst)
            
def t_books():
    lst=('10807374','10569855','2023013',)
    t_objs(Book,book_fmt,lst)

def t_movies():
    lst=('6799191','10772258','1291831','1424406')
    t_objs(Movie,movie_fmt,lst)

def test():
    t_persons()
    t_books()  
    t_movies()  

def t_none():
    lst=('11111',)    
    t_objs(Person,person_fmt,lst)    
