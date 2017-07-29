import json
import sys
import urllib.request
import urllib.error
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def elapp(request):
    (mid, text) = _decode_json(request) #接收來自Line客戶端的資料，包含ID和對話訊息
    _to_LINE_server(mid, text)
    if request.method == 'GET':
        return HttpResponse("GET")
    elif request.method == 'POST':
        return HttpResponse("POST")
        # return HttpResponse("POST")


def _decode_json(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    _mid = body["result"][0]["content"]["from"]
    _text = body["result"][0]["content"]["text"]
    return (_mid, _text)


def _to_LINE_server(_mid, _text):
    payload = {
        "to": [_mid],
        "toChannel": 1514282025,
        "eventType": "138311608800106203",
        "content": {
            "contentType": 1,
            "toType": 1,
            "text": _text
            # "text":body_unicode for debug(JSON object)
        }
    }

    req = urllib.request.Request("https://trialbot-api.line.me/v1/events",
                                 data=json.dumps(payload).encode('utf8'), #轉化json格式至文字訊息
                                 headers={
                                     "Content-type": "application/json; charset=UTF-8",
                                     "X-Line-ChannelID": "1514282025",
                                     "X-Line-ChannelSecret": "02837d87dca93447f810b8997336300f",
                                     "X-Line-Trusted-User-With-ACL": "Uc6b1dd894dd970e3eda68a0027332e52"
                                 })

    try:
        with urllib.request.urlopen(req) as response:
            print(response.read())
    except urllib.error.HTTPError as err:
        print(err)
