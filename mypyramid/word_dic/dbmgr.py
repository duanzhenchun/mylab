from pysqlite2 import dbapi2 as sqlite

class dbmanager:
  def __init__(self, out, dbname='word_dic.db'):
    #create a db file if not exist
    self.con = sqlite.connect(dbname)
    self.createtable(out)
    
  def __del__(self):
    self.con.close()

  def saveall(self,dic):
    for k,v in dic.iteritems():
        cmd = "insert or replace into %s values ('%s','%s')" % (self.tablename, k, v)
        self.con.execute(cmd)
    self.con.commit()   

  def clean(self):
    self.con.execute('drop table if exists %s' %self.tablename)
    self.con.commit()   
    
  def getall(self):
    dic={}
    cur = self.con.execute("select * from %s" %self.tablename)
    for row in cur:
        dic[row[0]]=eval(row[1])
    return dic    
        
  def createtable(self,name):
    self.tablename=name
    self.tbl_fmt='%s(word unique,freq integer)' %self.tablename
    self.con.execute('CREATE TABLE IF NOT EXISTS %s' %self.tbl_fmt)
    self.con.commit()
    
def test():
    db = dbmanager('tmp')
    dic={'abc':3,'eev':6}
    db.saveall(dic)
    db.saveall(dic)
    assert dic==db.getall()
    db.clean()
    
