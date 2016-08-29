# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.斷詞.拄好長度辭典揣詞 import 拄好長度辭典揣詞
from 臺灣言語工具.斷詞.語言模型揀集內組 import 語言模型揀集內組


class Moses服務:

    def __init__(self, 全部翻譯母語模型={}):
        self.全部翻譯母語模型 = 全部翻譯母語模型

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

        try:
            母語章物件 = (
                拆文分析器.建立章物件(整理後語句)
                .轉音(母語模型['拼音'])
                .揣詞(拄好長度辭典揣詞, 母語模型['辭典'])
                .揀(語言模型揀集內組, 母語模型['語言模型'])
                .翻譯(母語模型['摩西用戶端'])
            )
        except ConnectionRefusedError:
            return JsonResponse({'失敗': '服務啟動中，一分鐘後才試'})
        翻譯正規化結果 = 母語章物件.看分詞(
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

    @csrf_exempt
    def 標漢字音標(self, request):
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
        return self._標漢字音標實作(母語模型, 查詢語句)

    def _標漢字音標實作(self, 母語模型, 查詢語句):
        整理後語句 = 文章粗胚.數字英文中央全加分字符號(
            文章粗胚.建立物件語句前處理減號(母語模型['拼音'], 查詢語句)
        )

        try:
            母語章物件 = (
                拆文分析器.建立章物件(整理後語句)
                .轉音(母語模型['拼音'])
                .揣詞(拄好長度辭典揣詞, 母語模型['辭典'])
                .揀(語言模型揀集內組, 母語模型['語言模型'])
            )
        except ConnectionRefusedError:
            return JsonResponse({'失敗': '服務啟動中，一分鐘後才試'})
        翻譯正規化結果 = 母語章物件.看分詞(
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
