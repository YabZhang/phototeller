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
define('image_save_path', type=str, default='/tmp')


class BaseHandler(RequestHandler):
    """ TODO: Base Request Class """
    pass


class MainHandler(BaseHandler):

    def get(self):
        """ get """
        kwargs = {}
        kwargs['status'] = self.get_argument('status', False)
        kwargs['result'] = self.get_argument('result', '')
        kwargs['error'] = self.get_argument('error', '')
        self.render('index.html', **kwargs)

    def post(self):
        """ post """

        result='',
        error='',
        status=False

        if self.request.files:
            for field_name, files in self.request.files.items():
                for info in files:
                    filename, content_type = info['filename'], info['content_type']
                    body = info['body']
                    break    # 当前仅处理一份文件

            logging.info('%s %s %d bytes' % (filename, content_type, len(body)))
            if self._is_valid_image_file(content_type):
                result = self._handle_image_file(filename, body)
                status = True
            else:
                error = 'Invalid File Format! Please upload an image file!'

        else:
            error = 'No file found! Please upload an image file!'

        return self.render("index.html", status=status, result=result, error=error)

    def _is_valid_image_file(self, content_type):
        """ 检查文件类型是否匹配，这里只简单处理了文件类型 """
        if 'image' not in content_type:
            return False
        return True

    def _process_image_data(self, filename, image_data):
        """ TODO: 默认的图片处理逻辑, 在此处添加处理逻辑 """
        result = "filename: %s, length %s bytes" % (filename, len(image_data))
        return result

    def _handle_image_file(self, filename, raw_data, save=False):
        """ body 为文件原始数据，得到实时计算结果；或存储数据到文件; 默认不存储 """

        result = self._process_image_data(filename, raw_data)

        if save:
            if os.path.exists(options.image_save_path) and \
                    os.path.isdir(options.image_save_path):
                image_path = os.path.join(options.image_save_path, filename)
            else:
                image_path = os.path.join("/tmp", filename)

            try:
                with open(image_path, 'wb') as f:
                    f.write(raw_data)
            except Exception as e:
                logging.exception(e)

        return result




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
