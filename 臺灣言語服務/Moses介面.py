# -*- coding: utf-8 -*-
import Pyro4
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


class Moses介面:
    @property
    def 服務(self):
        pyro4主機 = getattr(settings, "PYRO4_TSU2_KI1", None)
        pyro4_naming主機 = Pyro4.locateNS(pyro4主機)
        pyro4的uri = pyro4_naming主機.lookup("Moses服務")
        return Pyro4.Proxy(pyro4的uri)

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
        except (KeyError, RuntimeError):
            查詢腔口 = '台語'
        try:
            查詢語句 = 連線參數['查詢語句']
        except KeyError:
            查詢語句 = '你好嗎？我很好！'
        try:
            return JsonResponse(self.服務.正規化翻譯實作(查詢腔口, 查詢語句))
        except Pyro4.errors.NamingError:
            return JsonResponse({'失敗': '服務無啟動，請通知阮！'}, status=503)
        except ConnectionRefusedError:
            return JsonResponse({'失敗': '服務啟動中，一分鐘後才試'}, status=503)

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
        except (KeyError, RuntimeError):
            查詢腔口 = '台語'
        try:
            查詢語句 = 連線參數['查詢語句']
        except KeyError:
            查詢語句 = '你好嗎？我很好！'
        try:
            return JsonResponse(self.服務.標漢字音標實作(查詢腔口, 查詢語句))
        except Pyro4.errors.NamingError:
            return JsonResponse({'失敗': '服務無啟動，請通知阮！'}, status=503)
        except ConnectionRefusedError:
            return JsonResponse({'失敗': '服務啟動中，一分鐘後才試'}, status=503)
