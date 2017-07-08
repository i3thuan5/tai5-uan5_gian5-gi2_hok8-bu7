# -*- coding: utf-8 -*-
import Pyro4
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.羅馬音仕上げ import 羅馬音仕上げ


class 文本介面:

    @classmethod
    @csrf_exempt
    def 漢字音標對齊(cls, request):
        if request.method == 'GET':
            連線參數 = request.GET
        else:
            連線參數 = request.POST
        try:
            腔口參數 = settings.HOK8_BU7_SIAT4_TING7[連線參數['查詢腔口']]
            漢字 = 連線參數['漢字']
            音標 = 連線參數['音標']
        except:
            return JsonResponse({'失敗': '參數有三个：查詢腔口、漢字、音標'}, status=403)
        try:
            return JsonResponse(cls.漢字音標對齊實作(腔口參數, 漢字, 音標))
        except Pyro4.errors.NamingError:
            return JsonResponse({'失敗': '服務無啟動，請通知阮！'}, status=503)
        except ConnectionRefusedError:
            return JsonResponse({'失敗': '服務啟動中，一分鐘後才試'}, status=503)

    @classmethod
    def 漢字音標對齊實作(cls, 腔口參數, 漢字, 音標):
        整理後漢字 = 文章粗胚.數字英文中央全加分字符號(
            文章粗胚.建立物件語句前處理減號(腔口參數['解析拼音'], 漢字)
        )
        整理後音標 = 文章粗胚.數字英文中央全加分字符號(
            文章粗胚.建立物件語句前處理減號(腔口參數['解析拼音'], 音標)
        )
        try:
            對齊物件 = 拆文分析器.對齊章物件(整理後漢字, 整理後音標)
        except:
            return {'失敗': '對齊失敗'}
        對齊結果 = {
            '分詞': 對齊物件.轉音(腔口參數['音標系統']).看分詞()
        }
        try:
            原音物件 = 對齊物件.轉音(腔口參數['音標系統'], 函式='轉閏號調')
            對齊結果['漢字'] = 羅馬音仕上げ.輕聲佮外來語(原音物件.看型(物件分詞符號=' '))
            對齊結果['音標'] = 羅馬音仕上げ.輕聲佮外來語(原音物件.看音())
        except:
            pass
        try:
            對齊結果['綜合標音'] = 對齊物件.綜合標音(腔口參數['字綜合標音'])
        except:
            pass
        return 對齊結果
