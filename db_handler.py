import sqlalchemy as db
from datetime import datetime

engine = db.create_engine('sqlite:///db/database.db')
connection = engine.connect()
metadata = db.MetaData()

# USERS table
users = db.Table('USERS', metadata, autoload=True, autoload_with=engine)

# FEED_TIME table
feed_time = db.Table('FEED_TIME', metadata, autoload=True, autoload_with=engine)


def insert_feed():
  now = datetime.now()
  query = db.insert(feed_time).values(DATE=now, QTY=1) 
  ResultProxy = connection.execute(query)

# Returns all Feedings
def get_feedings():
  query = db.select([feed_time])
  ResultProxy = connection.execute(query)
  ResultSet = ResultProxy.fetchall()
  print(ResultSet)
  

# Returns List of users
def get_users():
  query = db.select([users])
  ResultProxy = connection.execute(query)
  ResultSet = ResultProxy.fetchall()
  print(ResultSet)
