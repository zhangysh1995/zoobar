from zoodb import *
from debug import *

import bank_client
import profman_client
import hashlib
import os
import pbkdf2
import random

def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token

def login(username, password):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if not cred:
        return None
    password = pbkdf2.PBKDF2(password, cred.salt).hexread(32)
    if cred.password == password:
        return newtoken(db, cred)
    else:
        return None

def register(username, password):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred:
        return None
    salt = ''.join(map(lambda c: chr(ord(c) % 128), os.urandom(16)))
    newcred = Cred()
    newcred.username = username
    newcred.password = pbkdf2.PBKDF2(password, salt).hexread(32)
    newcred.salt = salt
    db.add(newcred)
    db.commit()

    persondb = person_setup()
    newperson = Person()
    newperson.username = username
    persondb.add(newperson)
    persondb.commit()

    bank_client.new(username)
    profman_client.new(username)

    return newtoken(db, newcred)

def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False

