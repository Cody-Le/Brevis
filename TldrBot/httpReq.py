import socketserver
from http.server import BaseHTTPRequestHandler
from brevis import brevis, shortPercent


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        output = ''
        output += '''<html>
            <head>
            <link rel="stylesheet" href="index.css">
            </head>
                <body><p>
                '''
        i = 0
        query = self.path.replace('%20', ' ')
        query = query.replace('/','')
        results = brevis.main(query)
        output += '<h1>Brevis: query:{}, {}% of all</h1>'.format(query,shortPercent)
        for suma in results:
            output += '<h3>[{}]</h3>{}<br>'.format(i, suma)
            i += 1
        output += '</p></body></html>'
        self.wfile.write(output.encode())




httpd = socketserver.TCPServer(("",8000), Handler)
httpd.serve_forever()
