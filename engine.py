from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import os
import toml

def build_engine():
  conf = load_configs()
  return create_engine('mysql+pymysql://%s:%s@%s/%s' % (conf["username"],
    conf["password"], conf["host"], conf["database"]))

def load_configs(config_file="config/database.toml"):
  config_file = os.path.dirname(os.path.realpath(__file__)) + "/" + config_file
  with open(config_file) as f:
    return toml.loads(f.read())

def session():
  return sessionmaker(bind=build_engine())()
