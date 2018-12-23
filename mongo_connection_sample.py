from datetime import datetime
from pymongo import MongoClient as Connection

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Sequence(tornado.web.RequestHandler):
    def get(self):
        db=self.application.database
        sequences = db["sequences"].find()

        for s in sequences:
            self.write("<br/>")
            self.write(s["sequence"])
            self.write(' - ' + s["id"])
            self.write(' at time: ' + str(s["time"]))

    def post(self):

        body = tornado.escape.json_decode(self.request.body)

        db=self.application.database

        new_sequence = {
            "id" : "1",
            "sequence" : body['sequence'],
            "time" : datetime.utcnow(),
        }

        db.sequences.insert(new_sequence)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/sequence", Sequence)
        ]

        settings = dict(
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.con = Connection('localhost', 27017)
        self.database = self.con["mongosample"]


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
