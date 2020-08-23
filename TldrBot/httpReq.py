import socketserver
from http.server import BaseHTTPRequestHandler
from brevis import brevis
from imgGet import imgGetter
from urllib.parse import urlparse
from urllib.parse import parse_qs



class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        if self.path != '/':
            parsed = urlparse('http://localhost:8080'+self.path)
            print(parse_qs(parsed.query))

            output = ''
            output += '''<html>
                        <head>
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Brevis</title>
                        </head>
                        <body style="font-family: san-serif;">
                            <p>
                            <h1 style="text-align: center;">Brevis</h1>
                            
                            '''
            i = 0
            pages = 15
            results = 5
            short = False;
            print(parse_qs(parsed.query))
            query = parse_qs(parsed.query).get('q')[0]
            print(query)
            if parse_qs(parsed.query).get('pgs'):
                pages = int(parse_qs(parsed.query).get('pgs')[0])
            if parse_qs(parsed.query).get('r'):
                results = int(parse_qs(parsed.query).get('r')[0])
            if parse_qs(parsed.query).get('short'):
                if parse_qs(parsed.query).get('short').lower() == 't' or parse_qs(parsed.query).get('short').lower() == 'true':
                    short= True

            brevisObj = brevis(query, lookAmt=pages, resultAmt=results, shortResult=short)
            results = brevisObj.main()
            img = imgGetter(query = query)
            output += '<h2 style= "text-align: center;">Query: {},  reduced by {}%</h2><br><h2 style="text-align: center;">Summary</h2><br><img src={}><div style="padding: 0px 400px 20px 400px;">'.format(query, results['percentage'], img.getImg())
            for suma in results['summary']:
                output += '<h3>[{}]</h3>{}<br>'.format(i, suma)
                i += 1
            output += '</div></p><h2 style="text-align: center;">Statistic</h2><table style="width: 60%;, text-align: center;"><tr><th>word</th><th>frequency</th></tr>'
            i = 0
            for key in sorted(results['wordRank'], key=results['wordRank'].get, reverse=True):
                if (i <= 20):
                    output += "<tr><td>" + key + "</td><td>" + str(results['wordRank'][key]) + "</td></tr>"
                    i += 1
                else:
                    break

            output += '</table><br><br><h2 style="text-align:center;">Citation</h2>'
            links = brevisObj.citation()
            if links != None:
                for link in brevisObj.citation():
                    output += f'<a href="{link}"><p>{link}<p></a>'
            else:
                output += '<p>links are not available</p>'
            output += '''
                        <style>
                            img{
                                position: relative;
                                left: 50%;
                                min-width: 30%;
                                transform: translateX(-50%);  
                            
                            }
                            
                            p, a{
                                text-align: center;
                            
                            }
                            h2{
                                text=aiign:center;
                            
                            }
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
            output += f'''<html><body>
                            <h1>
                                Brevis:Tl:dr bot
                            </h1>
                            <p>
                                To search, go to url 'http://localhost:{str(port)}' <br>
                                Add '/' + your query or topic wish to search <br>
                                example: 'http://localhost:{str(port)}/?q=" + benefit of chicken <br>
                                Result should be: 'http://localhost:{str(port)}/?q=benefit%20of%20chicken' (spaces are replaced by '%20')<br>
                                To change the number of results sentence and pages scan, default results = 5 and pages scan = 15<br>
                                Add '&r=' + the number of result and '&pgs=' + the number of page look up<br>
                                Template 'http://localhost:8080/?q=query&r=5&pgs=15'
                            </p>
                        </body></html>'''
            self.wfile.write(output.encode())



port = 8080
httpd = socketserver.TCPServer(("",port), Handler)
httpd.serve_forever()
