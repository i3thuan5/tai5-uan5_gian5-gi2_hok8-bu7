# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.斷詞.拄好長度辭典揣詞 import 拄好長度辭典揣詞
from 臺灣言語工具.斷詞.語言模型揀集內組 import 語言模型揀集內組
from 臺灣言語工具.語音合成.語音標仔轉換 import 語音標仔轉換
from 臺灣言語工具.解析整理.轉物件音家私 import 轉物件音家私


class 服務:

    def __init__(self, 全部翻譯母語模型={}, 全部合成母語模型={}):
        self.全部翻譯母語模型 = 全部翻譯母語模型
        self.全部合成母語模型 = 全部合成母語模型

    def 正規化翻譯支援腔口(self, request):
        全部翻譯母語 = sorted(self.全部翻譯母語模型.keys())
        return self.json包做回應({'腔口': 全部翻譯母語})

    @csrf_exempt
    def 正規化翻譯(self, request):
        if request.method == 'GET':
            連線參數 = request.GET
        else:
            連線參數 = request.POST
        try:
            查詢腔口 = 連線參數['查詢腔口']
            母語模型 = self.全部翻譯母語模型[查詢腔口]
        except:
            查詢腔口 = '閩南語'
            母語模型 = self.全部翻譯母語模型[查詢腔口]
        try:
            查詢語句 = 連線參數['查詢語句']
        except:
            查詢語句 = '你好嗎？我很好！'
        return self._正規化翻譯實作(母語模型, 查詢語句)

    def _正規化翻譯實作(self, 母語模型, 查詢語句):
        整理後語句 = 文章粗胚.數字英文中央全加分字符號(
            文章粗胚.建立物件語句前處理減號(母語模型['拼音'], 查詢語句)
        )
        華語章物件 = 拆文分析器.建立章物件(整理後語句)
        預設音標章物件 = 轉物件音家私.轉音(母語模型['拼音'], 華語章物件)
        揣詞章物件, _, _ = 拄好長度辭典揣詞.揣詞(母語模型['辭典'], 預設音標章物件)
        選好章物件, _, _ = 語言模型揀集內組.揀(母語模型['語言模型'], 揣詞章物件)

        try:
            母語章物件, _翻譯結構華語章物件, _分數 = 母語模型['摩西用戶端'].翻譯(選好章物件)
        except ConnectionRefusedError:
            return JsonResponse({'失敗': '服務啟動中，一分鐘後才試'})
        翻譯正規化結果 = 物件譀鏡.看分詞(
            母語章物件,
            物件分詞符號=' ', 物件分字符號='-', 物件分句符號=' '
        )
        翻譯結果 = {
            '翻譯正規化結果': 翻譯正規化結果
        }
        try:
            翻譯結果['綜合標音'] = 母語章物件.綜合標音(母語模型['字綜合標音'])
        except:
            pass
        return self.json包做回應(翻譯結果)

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
        母語章物件 = 拆文分析器.分詞章物件(查詢語句)
        音值物件 = 轉物件音家私.轉音(合成母語模型['拼音'], 母語章物件, 函式='音值')
        try:
            音值物件 = 合成母語模型['變調'].變調(音值物件)
        except:
            pass
        標仔陣列 = 語音標仔轉換.物件轉完整合成標仔(音值物件)
        愛合成標仔 = 語音標仔轉換.跳脫標仔陣列(標仔陣列)
        if 愛合成標仔 == []:
            愛合成標仔.append(語音標仔轉換.恬標仔())
        音檔 = 合成母語模型['模型'].合成(愛合成標仔)
#         調好音 = self.音標調音(查詢腔口, 音檔)
        return self.音檔包做回應(音檔.wav格式資料())

#     腔放送進度 = {偏漳優勢音腔口:1.0, 偏泉優勢音腔口:1.0,
#         混合優勢音腔口:1.0,
#         四縣腔:1.0, 海陸腔:1.05, 大埔腔:1.6,
#         饒平腔:1.02, 詔安腔:1.02, }
#
#     def 標仔合音檔(self, 查詢腔口, 標仔):
#         模型 = 全部合成母語模型[查詢腔口]
#         速度 = self.腔放送進度[查詢腔口]
#         音檔 = self.轉音檔.合成(模型, 速度, 標仔)
#         return 音檔

#     def 音標調音(self, 查詢腔口, 音檔):
#         if 查詢腔口.startswith(閩南語):
#             調好音 = self.音盒.篩雜訊(音檔)
#         elif 查詢腔口.startswith(客話):
#             調好音 = self.音盒.篩懸音(音檔, 6000)
#         else:
#             調好音 = 音檔
#         return 調好音

    def 文字包做回應(self, 文字):
        回應 = HttpResponse(文字)
        return 回應

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
