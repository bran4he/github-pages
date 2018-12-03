#!/usr/bin/python
import socket
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import sys
import logging
import logging.handlers

logger = logging.getLogger()

def initlog():
  LOG_FILE = "http.log"
  hdlr = logging.handlers.TimedRotatingFileHandler(LOG_FILE,when='D',interval=1,backupCount=40)
  formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
  hdlr.setFormatter(formatter)
  logger.addHandler(hdlr)

  logger.setLevel(logging.NOTSET)
  return logger

class MyHandler(SimpleHTTPRequestHandler):
  def do_POST(self):
    logger.info(self.path)
    logger.info(self.rfile.read(int(self.headers.getheader('Content-Length'))))
    if self.path.startswith('/password'):
      self.send_response(200)
      self.end_headers()
      self.wfile.write('Your IP address is %s' % self.client_address[0])
      return
    else:
      return
  def do_GET(self):
    return

class HTTPServerV6(HTTPServer):
  address_family = socket.AF_INET6

def main(argv):
  logger.info(argv)
  if len(argv) < 2:
    server = HTTPServerV6(('::', 8089), MyHandler)
    server.serve_forever()
  else:
    server = HTTPServerV6(('::', int(argv[1])), MyHandler)
    server.serve_forever()

if __name__ == '__main__':
  initlog()
  main(sys.argv)