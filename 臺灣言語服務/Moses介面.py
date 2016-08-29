# -*- coding: utf-8 -*-
import Pyro4
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class Moses介面:

    def __init__(self):
        self.服務 = Pyro4.Proxy("PYRONAME:Moses服務")

    def 正規化翻譯支援腔口(self, request):
        return JsonResponse({'腔口': self.服務.支援腔口()})

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
            return JsonResponse(self.服務.正規化翻譯實作(查詢腔口, 查詢語句))
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
            return JsonResponse(self.服務.標漢字音標實作(查詢腔口, 查詢語句))
        except ConnectionRefusedError:
            return JsonResponse({'失敗': '服務啟動中，一分鐘後才試'})
