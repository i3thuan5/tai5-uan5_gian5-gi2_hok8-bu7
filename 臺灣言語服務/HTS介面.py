# -*- coding: utf-8 -*-
from base64 import b64decode
import io

import Pyro4
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ranged_response import RangedFileResponse


from 臺灣言語服務.HTS服務 import HTS服務


class HTS介面:

    @property
    def 服務(self):
        if getattr(settings, "HTS_ING7_PYRO4", False):
            pyro4主機 = getattr(settings, "PYRO4_TSU2_KI1", None)
            pyro4_naming主機 = Pyro4.locateNS(pyro4主機)
            pyro4的uri = pyro4_naming主機.lookup("HTS服務")
            return Pyro4.Proxy(pyro4的uri)
        else:
            return HTS服務()

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
        except KeyError:
            查詢語句 = '你｜li2 好-無｜ho2-0bo5 ？｜? 我｜gua2 足｜tsiok4 好｜ho2 ！｜!'
        try:
            查詢腔口 = 連線參數['查詢腔口']
            if 查詢腔口 not in self.服務.支援腔口():
                raise RuntimeError()
        except (KeyError, RuntimeError):
            查詢腔口 = '閩南語'
        wav格式資料 = self.服務.語音合成實作(查詢腔口, 查詢語句)
        try:
            return self.音檔包做回應(request, b64decode(wav格式資料['data']))
        except TypeError:
            return self.音檔包做回應(request, wav格式資料)

    @csrf_exempt
    def 文本直接合成(self, request):
        if request.method == 'GET':
            連線參數 = request.GET
        else:
            連線參數 = request.POST
        try:
            查詢語句 = 連線參數['查詢語句']
        except KeyError:
            查詢語句 = '你｜li2 好-無｜ho2-0bo5 ？｜? 我｜gua2 足｜tsiok4 好｜ho2 ！｜!'
        try:
            查詢腔口 = 連線參數['查詢腔口']
            if 查詢腔口 not in self.服務.支援腔口():
                raise RuntimeError()
        except (KeyError, RuntimeError):
            查詢腔口 = '閩南語'
        wav格式資料 = self.服務.文本直接合成(查詢腔口, 查詢語句)
        try:
            return self.音檔包做回應(request, b64decode(wav格式資料['data']))
        except TypeError:
            return self.音檔包做回應(request, wav格式資料)

    def 音檔包做回應(self, request, 音檔):
        回應 = RangedFileResponse(
            request, io.BytesIO(音檔), content_type='audio/wav'
        )
        回應['Content-Disposition'] = 'filename="taiwanese.wav"'
        return 回應
