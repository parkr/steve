#!/usr/bin/env python

import daemon
import engine
import logging
import message
import os
import pid

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.escape import json_decode, json_encode
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("pidfile", default="/var/run/steve.%i.pid", help="file in which to store the server pid", type=str)

# mailgun
MAILGUN_OPTS = ["recipient", "sender", "from", "subject", "body-plain", "stripped-text",
  "timestamp", "signature", "message-headers"]

class MainHandler(tornado.web.RequestHandler):
    def head(self):
        pass

    def get(self):
        self.write("Nothing to see here quite yet...")

class MessagesFetchHandler(tornado.web.RequestHandler):
    def get(self):
      self.set_header("Content-Type", "application/json")
      self.write(json_encode( [m.as_json() for m in message.latest()] ))

class MessagesStoreHandler(tornado.web.RequestHandler):
    def post(self):
      attributes = self.extract_args_dict()
      logging.info("%s" % attributes)
      new_message = message.Message(attributes)
      session = engine.session()
      session.add(new_message)
      session.commit()

    def extract_args_dict(self):
      attributes = {}
      for opt in MAILGUN_OPTS:
        if self.json_args is not None:
          logging.info(("%s=\"%s\"" % (opt, self.json_args.get(opt))))
          attributes[opt] = self.json_args.get(opt)
        else:
          logging.info(("%s=\"%s\"" % (opt, self.get_arguments(opt))))
          attributes[opt] = self.get_arguments(opt)
      return attributes
    
    def prepare(self):
      self.json_args = None
      if self.request.headers.get("Content-Type") == "application/json":
        self.json_args = json_decode(self.request.body) 

def application():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/messages", MessagesFetchHandler),
    (r"/messages/store", MessagesStoreHandler)
  ])

def log_file_handler():
  log_file = 'log/tornado.%s.log' % options.port
  return open(os.path.join(os.path.dirname(os.path.abspath(__file__)), log_file), 'a+')

def daemonize(http_server):
  pidfile_path = options.pidfile % options.port
  pid.check(pidfile_path)
  log = log_file_handler()
  daemon_context = daemon.DaemonContext(stdout=log, stderr=log, working_directory='.')
  with daemon_context:
    pid.write(pidfile_path)

    # initialize the application
    http_server.listen(options.port)

    try:
      # enter the Tornado IO loop
        tornado.ioloop.IOLoop.instance().start()
    finally:
      # ensure we remove the pidfile
        pid.remove(pidfile_path)

def main():
    tornado.options.parse_command_line()
    daemonize(tornado.httpserver.HTTPServer(application()))

if __name__ == "__main__":
    main()
