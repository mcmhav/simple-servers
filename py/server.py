from http.server import BaseHTTPRequestHandler, HTTPServer

import logging
import sys
import getopt
import os
import json
import ast

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
LOGGER = logging.getLogger('tcpserver')


def logit(msg):
    """logit."""
    LOGGER.warning('Message: \n%s', msg)


SHOULD_401 = False


class Server(BaseHTTPRequestHandler):
    """S."""
    get_response = {
        'method': 'a get'
    }

    should_401 = False

    def _set_headers(self):
        self.send_response(self.response_status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        """do_GET."""
        logit("==================")
        logit(self.headers)

        # should_500 = self.path.endswith('/login')
        should_500 = False

        if should_500:
            self.send_response(500)
            self.end_headers()
        else:
            self._set_headers()

        json_response = json.dumps(self.get_response)

        self.wfile.write(json_response.encode())

    def do_HEAD(self):
        """do_HEAD."""
        self._set_headers()

    def do_POST(self):
        """do_POST."""
        logit("==================")
        logit(self.headers)

        logit(self.path.endswith('/api/equipment/queries'))
        logit(self.path.endswith('/login'))
        logit(self.path.endswith('login'))

        # if self.path.endswith('/api/equipment/queries'):
        #     self.should_401 = random.randint(0, 5) < 1

        # self.should_401 = self.path.endswith('/api/equipment/queries')
        self.should_401 = False

        if self.should_401 is True:
            self.send_response(401)
            self.send_header('location', 'http://localhost:3000/_gateway/user')
            self.end_headers()
        else:
            self._set_headers()

        json_response = json.dumps({
            'method': 'a post'
        })

        self.wfile.write(json_response.encode())
        return


def run(
    server_class=HTTPServer,
    handler_class=Server,
    port=80,
    get_response=None,
    response_status=None,
):
    """Run."""
    server_address = ('', port)

    if response_status is not None:
        handler_class.response_status = int(response_status)
    if get_response is not None:
        handler_class.get_response = ast.literal_eval(get_response)

    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def main(argv):
    """Main."""

    PORT = 3000
    GET_RESPONSE = None
    STATUS_CODE = 200

    try:
        opts, args = getopt.getopt(argv, "p:g:s:b", ["port="])
    except getopt.GetoptError:
        print('rairai, something wrong with inputz')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-p', '--port'):
            PORT = int(arg)
        elif opt in ('-g', '--GETresponse'):
            GET_RESPONSE = arg
        elif opt in ('-s', '--responseStatus'):
            STATUS_CODE = arg

    run(port=PORT, get_response=GET_RESPONSE, response_status=STATUS_CODE)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
