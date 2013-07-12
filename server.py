#!/usr/bin/env python

import engine
import logging
import message

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

# mailgun
MAILGUN_OPTS = ["recipient", "sender", "from", "subject", "body-plain", "stripped-text",
  "timestamp", "signature", "message-headers"]

adapter = engine.build_engine()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Nothing to see here quite yet...")

class MessagesStoreHandler(tornado.web.RequestHandler):
    def post(self):
      connection = adapter.connect()
      for opt in MAILGUN_OPTS:
        logging.info(("%s=%s" % (opt, self.get_arguments(opt))))

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/messages/store", MessagesStoreHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
