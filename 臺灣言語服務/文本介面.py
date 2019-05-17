# -*- coding: utf-8 -*-
import re

import Pyro4
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.羅馬字仕上げ import 羅馬字仕上げ
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
from 臺灣言語工具.音標系統.台語 import 新白話字
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


class 文本介面:
    # 目的：對漢羅語句內底揣出羅馬字
    # 有羅馬字：koo1娘 koo娘 koo1-niu5 koo-niû koo1-娘 姑-niu5 出--lai5
    # 無羅馬字：姑娘 g0v
    揣出羅馬字正規式 = re.compile(
        r'(['
        r'a-zA-Záàâǎāa̍a̋éèêěēe̍e̋íìîǐīı̍i̍i̋'
        r'óòôǒōo̍őó͘ò͘ô͘ǒ͘ō͘o̍͘ő͘úùûǔūu̍űḿm̀m̂m̌m̄m̍m̋ńǹn̂ňn̄n̍n̋ⁿ'
        r']+\d?)',
        flags=re.IGNORECASE
    )

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
        except KeyError:
            return JsonResponse({'失敗': '參數有三个：查詢腔口、漢字、音標'}, status=403)
        try:
            return JsonResponse(cls.漢字音標對齊實作(腔口參數, 漢字, 音標))
        except Pyro4.errors.NamingError:
            return JsonResponse({'失敗': '服務無啟動，請通知阮！'}, status=503)
        except ConnectionRefusedError:
            return JsonResponse({'失敗': '服務啟動中，一分鐘後才試'}, status=503)

    @classmethod
    @csrf_exempt
    def 羅馬字轉換(cls, request):
        if request.method == 'GET':
            連線參數 = request.GET
        else:
            連線參數 = request.POST
        try:
            語句參數 = 連線參數['查詢語句']
        except KeyError:
            return JsonResponse({'失敗': '參數愛有一个：查詢語句'}, status=403)
        try:
            return JsonResponse(cls.羅馬字轉換實作(語句參數))
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
        except 解析錯誤:
            return {'失敗': '對齊失敗'}
        對齊結果 = cls.章物件轉回應結果(腔口參數, 對齊物件.轉音(腔口參數['音標系統']))
        try:
            原音物件 = 對齊物件.轉音(腔口參數['音標系統'], 函式='轉閏號調')
            對齊結果['漢字'] = 羅馬字仕上げ.輕聲佮外來語(原音物件.看型(物件分詞符號=' '))
            對齊結果['音標'] = 羅馬字仕上げ.輕聲佮外來語(原音物件.看音())
        except 解析錯誤:
            pass
        return 對齊結果

    @classmethod
    def 章物件轉回應結果(cls, 腔口參數, 章物件):
        對齊結果 = {
            '分詞': 章物件.轉音(腔口參數['音標系統']).看分詞()
        }
        try:
            對齊結果['多元書寫'] = 腔口參數['多元書寫'].書寫章(章物件)
        except KeyError:
            pass
        try:
            對齊結果['綜合標音'] = 章物件.綜合標音(腔口參數['字綜合標音'])
        except KeyError:
            pass
        return 對齊結果

    @classmethod
    def 判斷羅馬字大小寫(cls, 羅馬字):
        # 總共輸出三種判斷：
        # 全小寫 首字大寫 全大寫
        結果 = '全小寫'
        if len(羅馬字) == 0:
            return None
        if 羅馬字[0].isupper():
            結果 = '首字大寫'
        # 如果輸入是數字調羅馬字，剔除數字調符
        if 羅馬字[-1].isnumeric():
            羅馬字 = 羅馬字[:-1]

        後半都是大寫 = True
        for 字母 in 羅馬字:
            # 後半若有字母毋是大寫，就當作後半全小寫
            if 字母 != 'ⁿ' and 字母.isupper() is False:
                後半都是大寫 = False
                break
        if 後半都是大寫:
            結果 = '全大寫'
        return 結果

    @classmethod
    def 調整閩南語羅馬字大小寫(cls, 原來音標, 轉過的羅馬字):
        大小寫 = cls.判斷羅馬字大小寫(原來音標)
        結果 = ''
        if 大小寫 == '首字大寫':
            結果 = 轉過的羅馬字[0].upper() + 轉過的羅馬字[1:]
        elif 大小寫 == '全大寫':
            for 字母 in 轉過的羅馬字:
                結果 += 字母.upper()
        elif 大小寫 == '全小寫':
            for 字母 in 轉過的羅馬字:
                結果 += 字母.lower()
        return 結果

    @classmethod
    def 羅馬字轉臺羅傳統調(cls, matchobj):
        揣著的羅馬字 = matchobj.group(0)
        白話字物件 = 新白話字(揣著的羅馬字)
        if 白話字物件.音標 is None:
            # 這是一个無合法的音標 免振動伊
            return 揣著的羅馬字
        暫存 = 白話字物件.轉換到臺灣閩南語羅馬字拼音()
        臺羅傳統調 = 臺灣閩南語羅馬字拼音(暫存).轉調符()
        結果 = cls.調整閩南語羅馬字大小寫(揣著的羅馬字, 臺羅傳統調)
        return 結果

    @classmethod
    def 臺羅傳統調轉白話字傳統調(cls, matchobj):
        揣著的臺羅 = matchobj.group(0)

        # 因為工具會將 N 轉作 nn，
        # 拄著大寫的臺羅『LÂNN』會將 NN 變作 nnnn
        # 就無法度正常轉出白話字。
        # 所以用工具轉換成白話字音標進前，
        # 做一寡事前準備：
        if 'NN' in 揣著的臺羅:
            轉換特殊符號的臺羅 = 揣著的臺羅.replace('NN', 'nn')
        else:
            轉換特殊符號的臺羅 = 揣著的臺羅

        臺羅物件 = 臺灣閩南語羅馬字拼音(轉換特殊符號的臺羅)
        if 臺羅物件.音標 is None:
            # 這是一个無合法的音標 免振動伊
            return 揣著的臺羅
        白話字傳統調 = 臺羅物件.轉白話字()
        結果 = cls.調整閩南語羅馬字大小寫(揣著的臺羅, 白話字傳統調)
        return 結果

    @classmethod
    def 羅馬字轉換實作(cls, 語句參數):
        # 使用者輸入漢羅語句，將羅馬字轉換出臺羅kah白話字傳統調。
        # （使用者會當輸入臺羅kah白話字的數字調抑是傳統調。）
        # 1. 掠出羅馬字的部份
        # 2. 用台灣言語工具判斷是毋是合法書寫的音標
        #   合法：轉調符
        #   無合法：照原本輸入的直接輸出
        # 3. 就提著一種音標結果矣。

        臺羅 = cls.揣出羅馬字正規式.sub(cls.羅馬字轉臺羅傳統調, 語句參數)
        白話字 = cls.揣出羅馬字正規式.sub(cls.臺羅傳統調轉白話字傳統調, 臺羅)
        return {
            '臺羅': 臺羅,
            '白話字': 白話字
        }
