import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep


class handler(BaseHTTPRequestHandler):
    # send a header...
    def sendHeader(self, code, mimetype):
        self.send_response(code)
        self.send_header('Content-type', mimetype)
        self.end_headers()

    # ---------------------------------------------------------
    # Handler for the GET requests
    def do_GET(self):
        assetsDir = "assets"
        asset = False

        try:
            # Check the file extension required and
            # set the right mime type

            sendReply = False
            if self.path.endswith(".html") or self.path.endswith("/"):
                print('dicks:' + self.path)
                mimetype = 'text/html'
                sendReply = True

            elif self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
                sendReply = True
                asset = True

            elif self.path.endswith(".png"):
                mimetype = 'image/png'
                sendReply = True
                asset = True

            elif self.path.endswith(".gif"):
                mimetype = 'image/gif'
                sendReply = True
                asset = True

            elif self.path.endswith(".js"):
                mimetype = 'application/javascript'
                sendReply = True
                asset = True

            elif self.path.endswith(".css"):
                mimetype = 'text/css'
                sendReply = True
                asset = True

            # It was a recognized type, send a reply

            if sendReply == True:

                # should we send an asset, or should we generate a page?
                if asset == True:
                    self.sendHeader(200, mimetype)
                    # Open the static file requested and send it
                    # assets all live in an asset directory

                    assetLocation = curdir + sep + assetsDir + sep + self.path

                    try:
                        f = open(assetLocation, 'rb')
                    except IOError:
                        self.send_error(404, 'Asset %s Not Found at : %s' % (self.path, assetLocation))
                        return

                    self.wfile.write(f.read())
                    f.close()

                else:
                    try:
                        self.sendHeader(200, mimetype)
                        # self.sendHeader(mimetype, 200)
                        method = getController('GET', self.path)
                        print('all g')
                        self.wfile.write(method())
                    except BaseException as e:

                        print(e)
                        print('e')

                        # doesn't seem to work for some reason...

                        self.send_error(404, 'Couldn\'t generate page for : %s' % self.path)
                        return

            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

        except ValueError:
            self.send_error(404, 'Couldn\'t find function from Routes file for path: %s' % self.path)

    # ---------------------------------------------------------
    # Handler for the POST requests
    def do_POST(self):

        # get all the interesting goodness from the incoming post
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': 'Content-Type',
                     },
            keep_blank_values=True
        )

        # move the cgi parameters (from the form) into a dictionary

        parameters = {}

        for key in form.keys():
            parameters[key] = form[key].value

        # create a response back to the web browser that
        # requested this page.
        # The reply should be a web page.

        # response headers

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # identify a function that should be called to generate
        # the web page
        method = getController('POST', self.path)

        # call it with the cgi parameters from the form,
        # return this value as the main page

        self.wfile.write(method(parameters))

        return


server = HTTPServer(('', 34567), handler)

def main():
    print('swag')

if __name__ == '__main__':
    try:
        print(curdir)
        main()
    except BaseException as e:
        print(e)
