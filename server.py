#!/usr/bin/env python

import engine
import logging
import message

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.escape import json_decode, json_encode
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

# mailgun
MAILGUN_OPTS = ["recipient", "sender", "from", "subject", "body-plain", "stripped-text",
  "timestamp", "signature", "message-headers"]

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Nothing to see here quite yet...")

class MessagesFetchHandler(tornado.web.RequestHandler):
    def get(self):
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
        logging.info(("%s=\"%s\"" % (opt, self.json_args.get(opt))))
        attributes[opt] = self.json_args.get(opt)
      return attributes
    
    def prepare(self):
      if self.request.headers.get("Content-Type") == "application/json":
        self.json_args = json_decode(self.request.body) 

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/messages", MessagesFetchHandler),
        (r"/messages/store", MessagesStoreHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
