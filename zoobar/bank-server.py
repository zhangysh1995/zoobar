#!/usr/bin/python

import rpclib
import sys
import bank
from debug import *

class BankRpcServer(rpclib.RpcServer):
    def rpc_new(self, username):
        return bank.new(username)

    def rpc_transfer(self, sender, recipient, zoobars):
        return bank.transfer(sender, recipient, zoobars)

    def rpc_balance(self, username):
        return bank.balance(username)

(_, dummy_zookld_fd, sockpath) = sys.argv

s = BankRpcServer()
s.run_sockpath_fork(sockpath)
