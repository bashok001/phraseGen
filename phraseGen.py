import json
import os
import random
import re

from cgi import parse_qs, escape
from time import sleep

from quote import *

template ="""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Quote Generator</title>

            <link rel="shortcut icon"
                  href="http://104.196.107.55:8080/staticAssets/images/pg_favicon.png">
            <link rel="stylesheet"
                  href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.no-icons.min.css">
            <link rel="stylesheet"
                  href="http://fonts.googleapis.com/css?family=Alice|Open+Sans:400,300,700">
            <link rel="stylesheet"
                  href="http://104.196.107.55:8080/staticAssets/css/styles.css">
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
                            <p class="lead text-center text-muted">
                                Augmented Backus Normal Form based quote generator. Uses NLTK
                                and Wordnet based nodebox linguistics library to create English
                                content.
                            </p>
                        </div>
                    </div>
                    <div class="row section topspace">
                        <div class="panel panel-cta">
                            <div class="panel-body">
                                <div class="quote" />
                            </div>
                        </div>
                    </div>
                    <div class="row section topspace">
                        <div class="col-lg-12 text-center">
                            <form method="POST" action="/quote">
                                <button type="submit"  class="btn btn-primary btn-lg">
                                    Get a new quote
                                </button>
                            </form>
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

            <script type="text/javascript"
                    src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.2.3.min.js"> </script>
            <script type="text/javascript"
                    src="http://104.196.107.55:8080/staticAssets/js/typed.min.js"> </script>
            <script>
                $(function(){
                    $('.quote').typed({
                        strings: ["%(genquote)s"],
                        typeSpeed: 20,
                        loop: true,
                        loopCount: 1,
                        showCursor: true,
                        cursorChar: "_",
                    });
                });
            </script>
            <!--[if lt IE 9]>
                <script src="http://104.196.107.55:8080/staticAssets/js/html5shiv.js"></script>
            <![endif]-->
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
        return showQuote(environ, start_response, router)
    else:
        return redirect_back(environ, start_response)

def redirect_back(environ, start_response):
    try:
        requestSize = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        requestSize = 0

    request = environ['wsgi.input'].read(requestSize)
    qs = parse_qs(request)
    seed = os.urandom(8).encode('hex')
    start_response('302 Found', [
        ('Location', '/' + 'quote' + '/' + seed)
    ])
    return []

def showQuote(environ, start_response, router):
    phrase = bnf.generatePretty(router.params['seed'])
    filtered = []

    for line in re.sub("<.*?>", " ", phrase).split("\n"):
        if len(line.strip()) > 0:
            filtered.append(line.strip())
        else:
            filtered.append("pause")

    print phrase

    response = pages['index']%{'genquote':phrase}

    start_response('200 OK', [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response)))
    ])

    return [response]
