#!/usr/bin/env python2

verbose = True

import symex.fuzzy as fuzzy
import __builtin__
import inspect
import symex.importwrapper as importwrapper
import symex.rewriter as rewriter

importwrapper.rewrite_imports(rewriter.rewriter)

import symex.symflask
import symex.symsql
import symex.symeval
import zoobar

def startresp(status, headers):
  if verbose:
    print 'startresp', status, headers

def report_balance_mismatch():
  print "WARNING: Balance mismatch detected"

def report_zoobar_theft():
  print "WARNING: Zoobar theft detected"

def adduser(pdb, username, token):
  u = zoobar.zoodb.Person()
  u.username = username
  u.token = token
  pdb.add(u)

def test_stuff():
  pdb = zoobar.zoodb.person_setup()
  pdb.query(zoobar.zoodb.Person).delete()
  adduser(pdb, 'alice', 'atok')
  adduser(pdb, 'bob', 'btok')
  user1 = pdb.query(zoobar.zoodb.Person).all()
  nuser1 = len(user1)
  balance1 = sum([p.zoobars for p in user1])
  pdb.commit()

  tdb = zoobar.zoodb.transfer_setup()
  tdb.query(zoobar.zoodb.Transfer).delete()
  tdb.commit()

  environ = {}
  environ['wsgi.url_scheme'] = 'http'
  environ['wsgi.input'] = 'xxx'
  environ['SERVER_NAME'] = 'zoobar'
  environ['SERVER_PORT'] = '80'
  environ['SCRIPT_NAME'] = 'script'
  environ['QUERY_STRING'] = 'query'
  environ['HTTP_REFERER'] = fuzzy.mk_str('referrer')
  environ['HTTP_COOKIE'] = fuzzy.mk_str('cookie')

  ## In two cases, we over-restrict the inputs in order to reduce the
  ## number of paths that "make check" explores, so that it finishes
  ## in a reasonable amount of time.  You could pass unconstrained
  ## concolic values for both REQUEST_METHOD and PATH_INFO, but then
  ## zoobar generates around 2000 distinct paths, and that takes many
  ## minutes to check.

  # environ['REQUEST_METHOD'] = fuzzy.mk_str('method')
  # environ['PATH_INFO'] = fuzzy.mk_str('path')
  environ['REQUEST_METHOD'] = 'GET'
  environ['PATH_INFO'] = 'trans' + fuzzy.mk_str('path')

  if environ['PATH_INFO'].startswith('//'):
    ## Don't bother trying to construct paths with lots of slashes;
    ## otherwise, the lstrip() code generates lots of paths..
    return

  resp = zoobar.app(environ, startresp)
  if verbose:
    for x in resp:
      print x

  ## Detect balance mismatch.
  ## When detected, call report_balance_mismatch()
  user2 = pdb.query(zoobar.zoodb.Person).all()
  nuser2 = len(user2)
  balance2 = sum([p.zoobars for p in user2])
  if nuser1 == nuser2 and balance1 != balance2:
    report_balance_mismatch()

  ## Detect zoobar theft.
  ## When detected, call report_zoobar_theft()
  transfers = tdb.query(zoobar.zoodb.Transfer).all()
  alice_balance = [alice.zoobars for alice in user2 if alice.username == 'alice'][0]
  bob_balance = [bob.zoobars for bob in user2 if bob.username == 'bob'][0]
  for user, zoobars in zip(['alice', 'bob'], [alice_balance, bob_balance]):
    did = len([t for t in transfers if t.sender == user]) != 0
    if not did and zoobars < 10:
      report_zoobar_theft()

fuzzy.concolic_test(test_stuff, maxiter=2000, verbose=1)

