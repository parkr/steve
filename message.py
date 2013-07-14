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

  def as_json(self):
    return {
        "id":              self.id,
        "recipient":       self.recipient,
        "sender":          self.sender,
        'who_from':        self.who_from,
        'subject':         self.subject,
        'body_plain':      self.body_plain,
        'stripped_text':   self.stripped_text,
        'timestamp':       self.timestamp,
        'signature':       self.signature,
        'message_headers': self.message_headers
    }

def latest():
  conn = engine.build_engine().connect()
  results = conn.execute(select([" * FROM messages"])).fetchall()
  return [build_message(r) for r in results]

def build_message(result):
  return Message({
      "id":              int(result[0]),
      "recipient":       result[1],
      "sender":          result[2],
      'who_from':        result[3],
      'subject':         result[4],
      'body_plain':      result[5],
      'stripped_text':   result[6],
      'timestamp':       result[7],
      'signature':       result[8],
      'message_headers': result[9]
  })

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
