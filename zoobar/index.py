from flask import g, render_template, request
from login import requirelogin
from debug import *
from zoodb import *

import profman_client

@catch_err
@requirelogin
def index():
    if 'profile_update' in request.form:
        profile = request.form['profile_update']
        profman_client.update(g.user.person.username, profile, g.user.token)

        ## also update the cached version (see login.py)
        g.user.person.profile = profile
    return render_template('index.html')
