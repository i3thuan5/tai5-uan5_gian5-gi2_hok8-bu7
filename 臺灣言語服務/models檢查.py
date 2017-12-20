from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
import json
from os.path import isfile

from django.core.exceptions import ValidationError


def 檢查敢是分詞(分詞):
    try:
        拆文分析器.分詞句物件(分詞)
    except 解析錯誤:
        raise ValidationError(
            '「{}」無法度解析做句物件'.format(分詞)
        )


def 檢查敢是影音檔案(影音所在):
    if not isfile(影音所在):
        raise ValidationError(
            '「{}」毋是檔案'.format(影音所在)
        )


def 檢查聽拍內底欄位敢有夠(聽拍):
    print(聽拍, type(聽拍))
    for 一逝 in json.loads(聽拍):
        print(一逝)
        for 欄位 in ['語者', '內容', '開始時間', '結束時間']:
            if 欄位 not in 一逝:
                raise ValidationError(
                    '「{}」無「{}」欄位'.format(一逝, 欄位)
                )
        if 一逝['開始時間'] < 0.0:
            raise ValidationError(
                '「{}」的開始時間「{}」是負的'.format(一逝, 一逝['開始時間'])
            )
