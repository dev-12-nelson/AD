import http.server
import socketserver
PORT = 8888
HOST = "localhost"
class MyHTTPHandler(http.server.SimpleHTTPRequestHandler):
	
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		self._set_headers()
		print(self.path)
		self.wfile.write("Hello World!".encode())
HTTP_server = socketserver.TCPServer((HOST, PORT), MyHTTPHandler, True)
HTTP_server.allow_reuse_address = True
HTTP_server.serve_forever()
