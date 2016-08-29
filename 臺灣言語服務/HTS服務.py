# -*- coding: utf-8 -*-
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.語音合成.語音標仔轉換 import 語音標仔轉換


class HTS服務:

    def __init__(self, 全部合成母語模型={}):
        self.全部合成母語模型 = 全部合成母語模型

    def 語音合成支援腔口(self, request):
        return self.json包做回應({'腔口': sorted(self.全部合成母語模型.keys())})

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
            合成母語模型 = self.全部合成母語模型[查詢腔口]
        except:
            查詢語句 = '你｜li2 好-無｜ho2-0bo5 ？｜? 我｜gua2 足｜tsiok4 好｜ho2 ！｜!'
            查詢腔口 = '閩南語'
            合成母語模型 = self.全部合成母語模型[查詢腔口]
        return self._語音合成實作(合成母語模型, 查詢語句)

    def _語音合成實作(self, 合成母語模型, 查詢語句):
        母語章物件 = (
            拆文分析器.分詞章物件(查詢語句)
            .轉音(合成母語模型['拼音'], 函式='音值')
        )
        try:
            音值物件 = 母語章物件.做(合成母語模型['變調'], '變調')
        except:
            音值物件 = 母語章物件
        標仔陣列 = 語音標仔轉換.物件轉完整合成標仔(音值物件)
        愛合成標仔 = 語音標仔轉換.跳脫標仔陣列(標仔陣列)
        if 愛合成標仔 == []:
            愛合成標仔.append(語音標仔轉換.恬標仔())
        音檔 = 合成母語模型['模型'].合成(愛合成標仔)
        return self.音檔包做回應(音檔.wav格式資料())

    def 音檔包做回應(self, 音檔):
        回應 = HttpResponse()
        回應.write(音檔)
        回應['Content-Type'] = 'audio/wav'
        回應['Content-Length'] = len(音檔)
        回應['Content-Disposition'] = 'filename="taiwanese.wav"'
        return 回應
