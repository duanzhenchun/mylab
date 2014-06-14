import bcrypt
from utils import *


def getDigest(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def isPassword(password, digest):
    return bcrypt.hashpw(password, digest) == digest

K_uid = 'onion_en_uid:'
def userid(n):
    return K_uid+n36id(n)

def test():
    password = 'dd'
    digest = '$2a$12$CUpYm3oJpkh5Whnxj6m/qetdSE56C4JCd9mp7qH1zVLmXLWJNpCfW'
    digest = '$2a$12$0IGnVFWEl0MvIINY6ZyB/usCdSKZhyOyYIc88JGdo1PRI733GUl3a'
    assert isPassword(password, digest )

if __name__ == "__main__":
    test()
