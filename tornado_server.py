# coding=utf-8
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import create_app
http_server = HTTPServer(WSGIContainer(create_app()))
http_server.listen(10086)  # flask默认的端口
IOLoop.instance().start() 
