from debug import *
from zoodb import *
import rpclib

def new(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        return c.call('new', username=username)

def transfer(sender, recipient, zoobars, token):
    with rpclib.client_connect('/banksvc/sock') as c:
        return c.call('transfer', sender=sender, recipient=recipient,
                zoobars=zoobars, token=token)

def balance(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        return c.call('balance', username=username)
