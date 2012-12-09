#models and security

from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    Text,
    Unicode,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )
from pyramid.security import (
    Allow,
    ALL_PERMISSIONS
    )
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import transaction

from zope.sqlalchemy import ZopeTransactionExtension

import logging
log = logging.getLogger(__name__)

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Editor(Base):
    __tablename__ = 'editors'
    id = Column(Integer, primary_key=True)
    persona_email = Column(Text, unique=True)
    is_admin = Column(Boolean, default=False)
    
    def __init__(self, persona_email, is_admin = False):
        self.persona_email = persona_email
        self.is_admin = is_admin
        

class RootFactory(object):
    """Simplest possible resource tree to map groups to permissions.
    """
    __acl__ = [
        (Allow, 'g:admin', ALL_PERMISSIONS),
        (Allow, 'g:editor', 'edit'),
    ]

    def __init__(self, request):
        self.request = request

def groupfinder(userid, request):
    log.debug('groupfinder %s', userid)
    query = DBSession.query(Editor).\
                filter(Editor.persona_email == userid)
    try:
        res = query.one()
        if res.is_admin:
            return ['g:admin']
        else:
            return ['g:editor']
    except NoResultFound:
        add_neweditor(userid)
        
def add_neweditor(userid):
    log.debug('add_neweditor %s', userid)
    editor = Editor(userid)
    try:
        DBSession.add(editor)
        DBSession.flush()
        transaction.commit()
    except IntegrityError:
        transaction.abort()
        log.error("database insert error, maybe editor name conflict.")
    except Exception, e:
        transaction.abort()
        log.error("database error!")
        
class OauthUser(Base):
    __tablename__ = 'oauthuser'
    id = Column(Integer, primary_key=True)  #auto set
    name = Column(Unicode(64), unique=True, nullable=False) #douban.com_1324242
    token = Column(Unicode(256), unique=True, nullable=False)   #token&secret

    def __init__(self, name, token):
        self.name = name
        self.token = token


        
