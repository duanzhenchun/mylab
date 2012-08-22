from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value

class User(object):
    def __init__(self, login, password, groups=None):
        self.login = login
        self.password = password
        self.groups = groups or []

    def check_password(self, passwd):
        return self.password == passwd
        

def _make_demo_user(login, **kw):
    kw.setdefault('password', login)
    USERS[login] = User(login, **kw)
    return USERS[login]

def groupfinder(userid, request):
    """group format g:XXX """
    user = USERS.get(userid)
    if user:
        return ['g:%s' % g for g in user.groups]
        
### INITIALIZE MODEL
USERS = {}
_make_demo_user('luser')
_make_demo_user('editor', groups=['editors'])
_make_demo_user('admin', groups=['admin'])

        
