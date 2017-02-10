from debug import *
from zoodb import *
import rpclib

def new(username):
    with rpclib.client_connect('/profmansvc/sock') as c:
        return c.call('new', username=username)

def get(username):
    with rpclib.client_connect('/profmansvc/sock') as c:
        return c.call('get', username=username)

def update(username, profile, token):
    with rpclib.client_connect('/profmansvc/sock') as c:
        return c.call('update', username=username, profile=profile,
                token=token)
