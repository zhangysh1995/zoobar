## This module wraps SQLalchemy's methods to be friendly to
## symbolic / concolic execution.

from fuzzy import *
import sqlalchemy.orm

oldget = sqlalchemy.orm.query.Query.get
def newget(query, primary_key):
  ## Find the object with the primary key "primary_key" in SQLalchemy
  ## query object "query", and do so in a symbolic-friendly way.
  ##
  ## Hint: given a SQLalchemy row object r, you can find the name of
  ## its primary key using r.__table__.primary_key.columns.keys()[0]
  ##
  ## The goal is to let concolic execution can try all possible
  ## records in a database.

  if isinstance(primary_key, concolic_int) or isinstance(primary_key, concolic_str):
    for r in query.all():
      new_primary_key = getattr(r, r.__table__.primary_key.columns.keys()[0])
      if isinstance(new_primary_key, int) or \
          isinstance(new_primary_key, str) or isinstance(new_primary_key, unicode):
            primary_key.__eq__(new_primary_key)

  return oldget(query, primary_key)

sqlalchemy.orm.query.Query.get = newget
