# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Pyro4 import Proxy


class Moses介面:

    def __init__(self):
        self.服務 = Proxy("PYRONAME:Moses服務")

    def 正規化翻譯支援腔口(self, request):
        return self.json包做回應({'腔口': self.服務.支援腔口()})

    @csrf_exempt
    def 正規化翻譯(self, request):
        if request.method == 'GET':
            連線參數 = request.GET
        else:
            連線參數 = request.POST
        try:
            查詢腔口 = 連線參數['查詢腔口']
            if 查詢腔口 not in self.服務.支援腔口():
                raise RuntimeError()
        except:
            查詢腔口 = '閩南語'
        try:
            查詢語句 = 連線參數['查詢語句']
        except:
            查詢語句 = '你好嗎？我很好！'
        try:
            return self._正規化翻譯實作(查詢腔口, 查詢語句)
        except ConnectionRefusedError:
            return JsonResponse({'失敗': '服務啟動中，一分鐘後才試'})

    @csrf_exempt
    def 標漢字音標(self, request):
        if request.method == 'GET':
            連線參數 = request.GET
        else:
            連線參數 = request.POST
        try:
            查詢腔口 = 連線參數['查詢腔口']
            if 查詢腔口 not in self.服務.支援腔口():
                raise RuntimeError()
        except:
            查詢腔口 = '閩南語'
        try:
            查詢語句 = 連線參數['查詢語句']
        except:
            查詢語句 = '你好嗎？我很好！'
        try:
            return self._標漢字音標實作(查詢腔口, 查詢語句)
        except ConnectionRefusedError:
            return JsonResponse({'失敗': '服務啟動中，一分鐘後才試'})

    def json包做回應(self, json):
        回應 = JsonResponse(json)
        return 回應

    def 音檔包做回應(self, 音檔):
        回應 = HttpResponse()
        回應.write(音檔)
        回應['Content-Type'] = 'audio/wav'
        回應['Content-Length'] = len(音檔)
        回應['Content-Disposition'] = 'filename="taiwanese.wav"'
        return 回應
