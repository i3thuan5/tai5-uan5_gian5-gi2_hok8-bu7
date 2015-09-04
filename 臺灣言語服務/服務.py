# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, JsonResponse
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.斷詞.拄好長度辭典揣詞 import 拄好長度辭典揣詞
from 臺灣言語工具.斷詞.語言模型揀集內組 import 語言模型揀集內組
from 臺灣言語服務.模型載入 import 全部翻譯母語模型
from 臺灣言語服務.模型載入 import 全部合成母語模型
from 臺灣言語工具.語音合成.語音標仔轉換 import 語音標仔轉換
import htsengine
from 臺灣言語工具.語音合成.音檔頭前表 import 音檔頭前表
from 臺灣言語工具.解析整理.轉物件音家私 import 轉物件音家私
from 臺灣言語工具.語音合成.閩南語變調 import 閩南語變調


class 服務:
    _粗胚 = 文章粗胚()
    _分析器 = 拆文分析器()
    _譀鏡 = 物件譀鏡()
    _揣詞 = 拄好長度辭典揣詞()
    _揀集內組 = 語言模型揀集內組()

    _家私 = 轉物件音家私()
    _閩南語變調 = 閩南語變調()
    _標仔轉換 = 語音標仔轉換()
    _音檔頭前表 = 音檔頭前表()

    def 正規化翻譯(self, request):
        try:
            查詢腔口 = request.POST['查詢腔口']
        except:
            查詢腔口 = '閩南語'
        try:
            查詢語句 = request.POST['查詢語句']
        except:
            查詢語句 = '壹 隻 好 e5 豬'
            查詢語句 = '語句匯入傷濟改'
            查詢語句 = '語句匯入太多次'

        母語模型 = 全部翻譯母語模型[查詢腔口]

        整理後語句 = self._粗胚.數字英文中央全加分字符號(
            self._粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 查詢語句)
        )
        華語章物件 = self._分析器.轉做章物件(整理後語句)
        預設音標章物件 = self._家私.轉音(母語模型['拼音'], 華語章物件)
        揣詞章物件, _, _ = self._揣詞.揣詞(母語模型['辭典'], 預設音標章物件)
        選好章物件, _, _ = self._揀集內組.揀(母語模型['語言模型'], 揣詞章物件)

        try:
            閩南語章物件, _翻譯結構華語章物件, _分數 = 母語模型['摩西用戶端'].翻譯(選好章物件)
        except ConnectionRefusedError:
            return JsonResponse({'失敗': '服務啟動中，一分鐘後才試'})
        翻譯結果 = self._譀鏡.看分詞(閩南語章物件,
                            物件分詞符號=' ', 物件分字符號='-', 物件分句符號='')
        return self.文字包做回應(翻譯結果)

    def 語音合成(self, request):
        try:
            查詢腔口 = request.POST['查詢腔口']
        except:
            查詢腔口 = '閩南語'
        try:
            查詢語句 = request.POST['查詢語句']
        except:
            查詢語句 = '語｜gu2 句｜ku3 匯-入｜hue7-lip8 傷｜siunn1 濟｜tse7 改｜kai2'
        母語章物件 = self._分析器.轉做章物件(查詢語句)

        合成母語模型 = 全部合成母語模型[查詢腔口]
        音值物件 = self._家私.轉音(合成母語模型['拼音'], 母語章物件, 函式='音值')
        變調物件 = self._閩南語變調.變調(音值物件)
        標仔陣列 = self._標仔轉換.物件轉完整合成標仔(變調物件)
        愛合成標仔 = self._標仔轉換.跳脫標仔陣列(標仔陣列)
        一點幾位元組, 一秒幾點, 幾个聲道, 原始取樣 = \
            htsengine.synthesize(合成母語模型['模型'], 愛合成標仔)
        音檔 = self._音檔頭前表.加起哩(原始取樣, 一點幾位元組, 一秒幾點, 幾个聲道)
#         調好音 = self.音標調音(查詢腔口, 音檔)
        return self.音檔包做回應(音檔)

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

    def 音檔包做回應(self, 音檔):
        回應 = HttpResponse()
        回應.write(音檔)
        回應['Content-Type'] = 'audio/wav'
        回應['Content-Length'] = len(音檔)
        回應['Content-Disposition'] = 'filename="voice.wav"'
        return 回應
