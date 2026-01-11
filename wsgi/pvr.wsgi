#psr.wsgi
DIR_PATH='/var/www/html/csv/'
POST_FILE='sfmonitor.csv'
import os
import re
import urllib.parse

def application(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    content = '0\n'
    csv = getcsv(environ)
    if chkprev(csv):
        with open(f'{DIR_PATH}{POST_FILE}', 'a', encoding='utf-8') as fp:
            print(csv, file=fp)
    return [content.encode()]

def chkprev(csv):
    prev = getprev()
    if csv.split(',')[9] != prev.split(',')[9]:
        putprev(csv)
        return True
    return False

def putprev(csv):
    with open(f'{DIR_PATH}{POST_FILE}.prev', 'w', encoding='utf-8') as fp:
        print(csv, file=fp)

def getprev():
    path = f'{DIR_PATH}{POST_FILE}.prev'
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as fp:
            return fp.read().rstrip('\n')
    return ''

def getcsv(environ):
    leng = int(environ.get('CONTENT_LENGTH', 0))
    inpt = environ['wsgi.input']
    msg = inpt.read(leng)
    dit = dict(urllib.parse.parse_qsl(msg))
    return dit[b'csvdata'].decode()

