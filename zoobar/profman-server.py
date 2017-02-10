#!/usr/bin/python

import rpclib
import sys
import auth_client

from zoodb import *
from debug import *

class ProfileRpcServer(rpclib.RpcServer):
    def rpc_new(self, username):
        profiledb = profile_setup()
        profile = profiledb.query(Profile).get(username)
        if profile:
            return False
        newprofile = Profile()
        newprofile.username = username
        profiledb.add(newprofile)
        profiledb.commit()
        
        return True

    def rpc_get(self, username):
        profiledb = profile_setup()
        profile = profiledb.query(Profile).get(username)
        return "" if profile is None else profile.profile

    def rpc_update(self, username, profile, token):
        profiledb = profile_setup()
        profilep = profiledb.query(Profile).get(username)

        # username is not found.
        if profilep is None:
            return False
        
        # invalid token.
        if not auth_client.check_token(username, token):
            return False

        profilep.profile = profile
        profiledb.commit()

        return True

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ProfileRpcServer()
s.run_sockpath_fork(sockpath)
