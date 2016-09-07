# -*- coding: utf-8 -*-
from base64 import b64decode

import Pyro4
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


class HTS介面:

    def __init__(self):
        self.服務 = Pyro4.Proxy("PYRONAME:HTS服務")

    def 語音合成支援腔口(self, request):
        return JsonResponse({'腔口': self.服務.支援腔口()})

    @csrf_exempt
    def 語音合成(self, request):
        if request.method == 'GET':
            連線參數 = request.GET
        else:
            連線參數 = request.POST
        try:
            查詢語句 = 連線參數['查詢語句']
        except:
            查詢語句 = '你｜li2 好-無｜ho2-0bo5 ？｜? 我｜gua2 足｜tsiok4 好｜ho2 ！｜!'
        try:
            查詢腔口 = 連線參數['查詢腔口']
            if 查詢腔口 not in self.服務.支援腔口():
                raise RuntimeError()
        except:
            查詢腔口 = '閩南語'
        wav格式資料 = self.服務.語音合成實作(查詢腔口, 查詢語句)
        return self.音檔包做回應(b64decode(wav格式資料['data']))

    def 音檔包做回應(self, 音檔):
        回應 = HttpResponse()
        回應.write(音檔)
        回應['Content-Type'] = 'audio/wav'
        回應['Content-Length'] = len(音檔)
        回應['Content-Disposition'] = 'filename="taiwanese.wav"'
        return 回應
