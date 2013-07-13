import engine

from sqlalchemy.sql import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()

class Message(Base):
  __tablename__ = 'messages'

  id         = Column(Integer, primary_key=True)
  recipient  = Column(String(255))
  sender     = Column(String(255))
  who_from   = Column(String(255))
  subject    = Column(String(255))
  body_plain = Column(Text)
  stripped_text = Column(Text)
  timestamp  = Column(Integer)
  signature  = Column(String(255))
  message_headers = Column(Text)

  def __init__(self, attributes):
    for key in attributes.keys():
      setattr(self, key, attributes[key])

  def __repr__(self):
    return "<Message('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

def latest():
  conn = engine.build_engine().connect()
  s = select([" * FROM messages"])
  return conn.execute(s)

if __name__ == "__main__":
  e = engine.build_engine()

  metadata = MetaData(bind=e)
  messages_table = Table('messages', metadata,
    Column('id', Integer, primary_key=True),
    Column('recipient', String(255)),
    Column('sender', String(255)),
    Column('who_from', String(255)),
    Column('subject', String(255)),
    Column('body_plain', Text),
    Column('stripped_text', Text),
    Column('timestamp', Integer),
    Column('signature', String(255)),
    Column('message_headers', Text),
  )

  metadata.create_all()
