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
from contextlib import closing

TEMPLATE=('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
'<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja" dir="ltr">'
'<head>'
'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
'<meta http-equiv="pragma" content="no-cache" />'
'<meta http-equiv="cache-control" content="no-cache" />'
'<meta http-equiv="Expires" content="-1" />'
'<meta http-equiv="Content-Style-Type" content="text/css" />'
'<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">'
'<title>- ホームエネルギーモニタリングサービス -</title>'
'<link href="{docroot}css/rt_import.css" rel="stylesheet" type="text/css" media="all" />'
'<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>'
'<script type="text/javascript">'
'function setcontent() {'
'  $.getJSON("{uri}?json" , function(data) {'
'    $("#katta").text(data.added_buypower + "W");'
'    $("#hatsu").text(data.added_power + "W");'
'    $("#uttaw").text(data.added_sellpower + "W");'
'    $("#shohi").text(data.syohi + "W");'
'    $("#shiyo").text(data.shiyo + "W");'
'  });'
'}'
'$(function() {setcontent();/*auto*/});'
'</script>'
'</head>'
'<body>'
'<div id="Container2">'
'<div id="PopUpContents">'
'<dl class="relationBlock" id="btn_l">'
'<dd><a onclick="setcontent();">'
'<img id="btn_r_img" src="{docroot}images/manu_in.png" width="90" height="26" /></a></dd></dl>'
'<dl class="relationBlock" id="btn_r">'
'<dd><a href="{uri}{prm}">'
'<img id="btn_r_img" src="{docroot}images/auto_{onoff}.png" width="90" height="26" /></a></dd></dl>'
'<dl class="relationBlock" id="rSell">'
'<dd><span class="numTxt" id="katta"></span></dd></dl>'
'<dl class="relationBlock" id="rBuy">'
'<dd><span class="numTxt" id="hatsu"></span></dd></dl>'
'<dl class="relationBlock" id="rEPG">'
'<dd><span class="numTxt" id="uttaw"></span></dd></dl>'
'<dl class="relationBlock" id="rConsumption">'
'<dd><span class="numTxt" id="shohi"></span></dd></dl>'
'<dl class="relationBlock" id="rUse">'
'<dd><span class="numTxt" id="shiyo"></span></dd></dl>'
'<!-- / #PopUpContents --></div>'
'<!-- / #Container --></div>'
'</body>'
'</html>')

AUTOREF='setInterval(function(){setcontent();}, 1000);'

def application(environ, start_response):
    url = f'http://{IP_ADDRESS}/GetMonitoringData.cgi'
    try:
        query = environ.get('QUERY_STRING')
        if 'json' in query:
            content_type = 'text/json;'
            content = getjson(url)
        else:
            content_type = 'text/html;'
            uri = environ.get('REQUEST_URI').replace('?auto', '')
            temp = TEMPLATE.replace('{docroot}', DOC_ROOT).replace('{uri}', uri)
            if 'auto' in query:
                content = temp.replace('/*auto*/', AUTOREF).replace('{prm}','').replace('{onoff}', 'on')
            else:
                content = temp.replace('{prm}', '?auto').replace('{onoff}', 'off')
    except Exception as e:
        content = list(traceback.TracebackException.from_exception(e).format())[-1] + url
    start_response('200 OK', [('Content-type', content_type + ' charset=utf-8')])
    return [content.encode()]

def getjson(url):
    jobj = getweb(url)
    jmap = dict(jobj)
    jmap.update({ "syohi": getsyohi(jobj) })
    jmap.update({ "shiyo": getshiyo(jobj) })
    return json.dumps(jmap)

def getsyohi(jobj):
    # 発電電力量－売電力量＋買電力量
    hatsu = float(jobj['added_power'])
    sel = float(jobj['added_sellpower'])
    kai = float(jobj['added_buypower'])
    syohi = hatsu - sel + kai
    return f'{syohi:.2f}'

def getshiyo(jobj):
    # 発電電力量－売電力量
    hatsu = float(jobj['added_power'])
    sel = float(jobj['added_sellpower'])
    hiyo = hatsu - sel
    return f'{hiyo:.2f}'

def getweb(url):
    req = urllib.request.Request(url)
    with closing(urllib.request.urlopen(req)) as res:
        mobj = re.search(r'{.*}', res.read().decode())
        jobj = json.loads(mobj.group())
        return jobj

