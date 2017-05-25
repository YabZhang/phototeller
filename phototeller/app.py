#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TODO: DOC
"""

import os
import logging

from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line

logging.basicConfig(
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="[%(name)s][%(levelname)s][%(asctime)s]: %(message)s")

define('debug', type=bool, default=True, help='server run in debug mode; default debug=True')
define('port', type=int, default=8080, help='server run on the given port; default port=8080')
define('static_path', type=str, default='static')
define('template_path', type=str, default='templates')


class BaseHandler(RequestHandler):
    """ Base Request Class """
    pass


class MainHandler(BaseHandler):

    def get(self, *args, **kwargs):
        """ get """
        self.render('index.html')

    def post(self):
        """ post """
        file_name = []
        print('request: ', self.request)
        if self.request.files:
            for field_name, files in self.request.files.itmes():
                for info in files:
                    filename, content_type = info['filename'], info['content_type']
                    body = info['body']
                    print('POST "%s" "%s" %d bytes',
                                 filename, content_type, len(body))
        self.redirect('/')


def url_collector():
    """ url gather """
    return (
        ('/', MainHandler),
    )


def main():
    """ main: all start from here... """

    # parse config
    parse_command_line()
    # gather urls
    urls = url_collector()
    # web settings
    settings = {
        'debug': options.debug,
        'cookie_secret': '__guessme__',
        'xsrf_token': '__guessme__',
        'static_path': os.path.join(os.path.dirname(__file__), options.static_path),
        'template_path': os.path.join(os.path.dirname(__file__), options.template_path)
    }

    app = Application(urls, **settings)
    app.listen(port=options.port, address='0.0.0.0')
    IOLoop.current().start()


if __name__ == '__main__':
    main()
