from pysqlite2 import dbapi2 as sqlite

class dbmanager:
  def __init__(self,dbname):
    #create a db file if not exist
    self.con = sqlite.connect(dbname)
    
  def __del__(self):
    self.con.close()

  def save(self,tablename,vlst,cmt):
    cmd='insert or replace into %s values (%s)' %(tablename, ','.join(('?')*len(vlst)))
    self.con.execute(cmd, vlst)
    if cmt:    
        self.con.commit()   
        
  def load(self,tablename, iD):
    cur = self.con.execute('select * from %s where id="%s"' %(tablename,iD))
    return cur.fetchone()
    
  def clean(self,tablename):
    self.con.execute('drop table if exists %s' %tablename)
    self.con.commit()   
    
  def createtable(self,tbl_fmt):
    self.con.execute('CREATE TABLE IF NOT EXISTS %s' %tbl_fmt)
    self.con.commit()
  
  def commit(self):
    self.con.commit()
    
def test():
    db = dbmanager('tmp')
    db.clean()
    
