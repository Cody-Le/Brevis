import socketserver
from http.server import BaseHTTPRequestHandler
from brevis import brevis
from imgGet import imgGet




class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        if self.path != '/':
            output = ''
            output += '''<html>
                        <head>
                            <title>Brevis</title>
                        </head>
                        <body style="font-family: san-serif;">
                            <p>
                            <h1 style="text-align: center;">Brevis</h1>
                            
                            '''
            i = 0
            query = self.path.replace('%20', ' ')
            query = query.replace('/', '')
            brevisObj = brevis(query)
            results = brevisObj.main()
            img = imgGet(query = query)
            output += '<h2 style= "text-align: center;">Query: {},  summarize to {}%</h2><br><h2>Summary</h2><br><img src={}><div style="padding: 200px;">'.format(query, results['percentage'], img.getImg())
            for suma in results['summary']:
                output += '<h3>[{}]</h3>{}<br>'.format(i, suma)
                i += 1
            output += '</div></p><h2>Statistic</h2><table style="width: 60%;"><tr><th>word</th><th>frequency</th></tr>'
            i = 0
            for key in sorted(results['wordRank'], key=results['wordRank'].get, reverse=True):
                if (i <= 20):
                    output += "<tr><td>" + key + "</td><td>" + str(results['wordRank'][key]) + "</td></tr>"
                    i += 1
                else:
                    break

            output += '</table>'
            output += '''
                        <style>
                            table{
                                position: relative;
                                left: 50%;
                                transform: translateX(-50%);
                                border-collapse: collapse;
                            }
                            table, th, td{
                                border: 1px solid black; 
                            }
                        
                        </style></body></html>'''
            self.wfile.write(output.encode())
        else:
            output = ''
            output += '''<html><body>
                            <h1>
                                Brevis:Tl:dr bot
                            </h1>
                            <p>
                                To search, go to url 'http://localhost:{}' <br>
                                Add '/' + your query or topic wish to search <br>
                                example: 'http://localhost:{}/" + benefit of chicken <br>
                                result should be: 'http://localhost:{}/benefit%20of%chicken' (spaces are replaced by '%20')<br>
                            </p>
                        
                        </body></html>'''.format(str(port), str(port), str(port))
            self.wfile.write(output.encode())



port = 8080
httpd = socketserver.TCPServer(("",port), Handler)
httpd.serve_forever()
