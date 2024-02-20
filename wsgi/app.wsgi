#app.wsgi
IP_ADDRESS='192.168.0.41'
DOC_ROOT='/'
#DOC_ROOT='https://www.frontier-monitor.com/persite/'

import os
import re
import sys
import json
import traceback
import urllib.request

TEMPLATE=('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
'<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja" dir="ltr">'
'<head>'
'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
'{refresh}'
'<meta http-equiv="pragma" content="no-cache" />'
'<meta http-equiv="cache-control" content="no-cache" />'
'<meta http-equiv="Expires" content="-1" />'
'<meta http-equiv="Content-Style-Type" content="text/css" />'
'<title>- ホームエネルギーモニタリングサービス -</title>'
'<link href="{docroot}css/rt_import.css" rel="stylesheet" type="text/css" media="all" />'
'</head>'
'<body>'
'<div id="Container2">'
'<div id="PopUpContents">'
'<dl class="relationBlock" id="btn_l">'
'<dd><a href="{uri}">'
'<img id="btn_r_img" src="{docroot}images/manu_in.png" width="90" height="26" /></a></dd></dl>'
'<dl class="relationBlock" id="btn_r">'
'<dd><a href="{uri}?auto">'
'<img id="btn_r_img" src="{docroot}images/auto_{onoff}.png" width="90" height="26" /></a></dd></dl>'
'<dl class="relationBlock" id="rSell">'
'<dd><span class="numTxt" id="katta"></span>{0}W</dd></dl>'
'<dl class="relationBlock" id="rBuy">'
'<dd><span class="numTxt" id="hatsu"></span>{1}W</dd></dl>'
'<dl class="relationBlock" id="rEPG">'
'<dd><span class="numTxt" id="uttaw"></span>{2}W</dd></dl>'
'<dl class="relationBlock" id="rConsumption">'
'<dd><span class="numTxt" id="shohi"></span>{3}W</dd></dl>'
'<dl class="relationBlock" id="rUse">'
'<dd><span class="numTxt" id="shiyo"></span>{4}W</dd></dl>'
'<!-- / #PopUpContents --></div>'
'<!-- / #Container --></div>'
'</body>'
'</html>')

AUTOREF='<meta http-equiv="refresh" content="1; URL=">'

def application(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])
    query = environ.get('QUERY_STRING')
    uri = environ.get('REQUEST_URI').replace('?auto', '')
    temp = TEMPLATE.replace('{docroot}', DOC_ROOT)
    temp = temp.replace('{uri}', uri)
    temp = temp.replace('{refresh}', AUTOREF if query == 'auto' else '')
    temp = temp.replace('{onoff}', 'on' if query == 'auto' else 'off')
    url = f'http://{IP_ADDRESS}/GetMonitoringData.cgi'
    try:
        jobj = getweb(url)
        content = temp.replace('{0}', jobj['added_buypower']) \
            .replace('{1}', jobj['added_power']) \
            .replace('{2}', jobj['added_sellpower']) \
            .replace('{3}', getsyohi(jobj)) \
            .replace('{4}', getshiyo(jobj))
    except Exception as e:
        content = list(traceback.TracebackException.from_exception(e).format())[-1] + url
    return [content.encode()]

def getsyohi(jobj):
    # 発電電力量－売電力量＋買電力量
    hatsu = float(jobj['added_power'])
    uri = float(jobj['added_sellpower'])
    kai = float(jobj['added_buypower'])
    syohi = hatsu - uri + kai
    return f'{syohi:.2f}'

def getshiyo(jobj):
    # 発電電力量－売電力量
    hatsu = float(jobj['added_power'])
    uri = float(jobj['added_sellpower'])
    hiyo = hatsu - uri
    return f'{hiyo:.2f}'

def getweb(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        mobj = re.search(r'{.*}', res.read().decode())
        jobj = json.loads(mobj.group())
        return jobj

