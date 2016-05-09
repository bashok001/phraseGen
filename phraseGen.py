import json
import os
import random
import re

from cgi import parse_qs, escape
from time import sleep

template = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Quote Generator</title>

            <link rel="shortcut icon" href="http://127.0.0.1/staticAssets/images/pg_favicon.png">
            <link href="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.no-icons.min.css" rel="stylesheet">
            <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Alice|Open+Sans:400,300,700">
            <link rel="stylesheet" href="http://127.0.0.1/staticAssets/css/styles.css">

        </head>
        <body class="home">

        <header id="header">
            <div style="background-position: 50%% 0px;">
                <h1 id="logo" class="text-center">
                    <span class="title">Quote generator</span>
                </h1>
            </div>
        </header>

        <main id="main">
            <div class="container">
                <div class="row section topspace">
                    <div class="col-md-12">
                        <p class="lead text-center text-muted">Python based, Backus Normal Form, quote generator.
                        Uses NLTK and Wordnet based nodebox linguistics library to create English content. </p>
                    </div>
                </div>
                <div class="row section topspace">
                    <div class="panel panel-cta">
                        <div class="panel-body">
                            <div class="quote" />
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <footer id="footer" />

        <footer id="underfooter">
            <div class="container">
                <div class="row">
                    <div class="col-md-6 widget">
                        <div class="widget-body">
                            <p>CIS 668 (Natural Language Generation)</p>
                        </div>
                    </div>
                    <div class="col-md-6 widget">
                        <div class="widget-body">
                            <p class="text-right">Copyright &#169; 2016, Cynic Inc.<br> </p>
                        </div>
                    </div>
                </div>
            </div>
        </footer>

        <script src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.2.3.min.js" type="text/javascript"></script>
        <script src="http://127.0.0.1/staticAssets/js/typed.min.js" type="text/javascript"></script>
        <script>
            $(function(){
                $('.quote').typed({
                    strings: ["%(genquote)s"],
                    typeSpeed: 30,
                    loop: true,
                    loopCount: 2,
                    showCursor: true,
                    cursorChar: "|",
                });
            });
        </script>
        <!--[if lt IE 9]> <script src="http://127.0.0.1/staticAssets/js/html5shiv.js"></script> <![endif]-->

        </body>
    </html>
"""

pages = {
     'index' : template
}

class Router():
    def __init__(self, url):
        self.url = url

    def match(self, pattern):
        match = re.search(pattern, self.url)
        if match:
            self.params = match.groupdict()
            return True
        else:
            return False

def application(environ, start_response):
    url = environ['PATH_INFO']
    router = Router(url)

    if router.match('^/(?P<type>quote)/(?P<seed>[0-9a-zA-Z]+)$'):
        return show_quote(environ, start_response, router)
    else:
        return redirect_back(environ, start_response)

def redirect_back(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    qs = parse_qs(request_body)
    seed = os.urandom(8).encode('hex')
    start_response('302 Found', [
        ('Location', '/' + 'quote' + '/' + seed)
    ])
    return []

def show_quote(environ, start_response, router):
    #p,str_seed = bnf.generatePretty('<' + router.params['type'] + '>',router.params['seed'])
    phrase = "a big phrase"
    filtered = []

    for line in re.sub("<.*?>", " ", phrase).split("\n"):
        if len(line.strip()) > 0:
            filtered.append(line.strip())
        else:
            filtered.append("pause")

    response_body = pages['index']%{'genquote':phrase}
    # % {
    #     'poem': p,
    #     'url': router.url,
    #     'lines': json.dumps(filtered)
    # }

    start_response('200 OK', [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ])

    return [response_body]
