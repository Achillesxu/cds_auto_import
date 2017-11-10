#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
desc： 后台服务, 定时扫描ResTable里面的数据，通过数码的接口查询结果，如果注入媒资成功，则将按照预定的数据项写入mysql的url表中，
       并更新ResTable表，
time：2017-05-15
author: achilles_xushy
"""
import sys
import logging
import time
import signal

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.log

from web_server import loop_check_inject

__author__ = 'achilles_xushy'

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s－%(asctime)s-%(module)s-%(filename)s-%(funcName)s-'
                           '[line:%(lineno)d]-%(message)s')

root_myapp = logging.getLogger('web_server')
root_myapp.propagate = False
stdout_info = logging.StreamHandler(stream=sys.stdout)
stdout_formatter = logging.Formatter(
    '%(name)s-%(levelname)s－%(asctime)s-%(module)s-%(filename)s-%(funcName)s-[line:%(lineno)d]-%(message)s')
stdout_info.setFormatter(stdout_formatter)
root_myapp.addHandler(stdout_info)
root_myapp.setLevel(logging.INFO)

tornado.log.LogFormatter(fmt='[%(levelname)1.1s %(asctime)s %(module)s-%(funcName)s-%(lineno)d] %(message)s',
                         datefmt='%y-%m-%d %H:%M:%S')

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 10


class Application(tornado.web.Application):
    def __init__(self):
        # import handler
        from web_server.handler import transfer_status
        from web_server.handler import inject_status
        from web_server.handler import media_search

        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "web_server/static"),
            autoescape=None,
            # debug=True,
        )

        handlers = [
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r'/inject_status', inject_status.InjectStatusHomePage),  # homepage entrance
            (r'/delete_record', inject_status.DeleteInjectRecord),
            (r'/data_search', media_search.DatabaseSearch),
            (r'/media_search', media_search.MediaSearch),
            (r'/delete_search', media_search.SearchDelete),
            (r'/TransferStatus', transfer_status.TransferStatus)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)


def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    logging.info('Stopping http server')
    server.stop()

    logging.info('Will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logging.info('Shutdown')

    stop_loop()


def main():
    try:
        port = int(sys.argv[1])
    except:
        # port = 8888
        port = 15001

    global server

    server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    server.listen(port)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    t_p_call = tornado.ioloop.PeriodicCallback(loop_check_inject.loop_check_inject_insert_mysql, 1000 * 60 * 5)
    t_p_call.start()
    tornado.ioloop.IOLoop.instance().start()

    logging.info("Exit...")


if __name__ == "__main__":
    main()
