from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
from os.path import isfile
import wave

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


def 檢查敢是wav(影音所在):
    try:
        with wave.open(影音所在, 'rb'):
            pass
    except wave.Error:
        raise ValidationError(
            '「{}」毋是wav'.format(影音所在)
        )
    except IsADirectoryError:
        raise ValidationError(
            '「{}」毋是檔案'.format(影音所在)
        )


def 檢查聽拍內底欄位敢有夠(聽拍):
    for 一逝 in 聽拍:
        for 欄位 in ['語者', '內容', '開始時間', '結束時間']:
            if 欄位 not in 一逝:
                raise ValidationError(
                    '「{}」無「{}」欄位'.format(一逝, 欄位)
                )
        try:
            拆文分析器.分詞句物件(一逝['內容'])
        except 解析錯誤 as 錯誤:
            raise ValidationError(
                '「{}」無法度正確解析：{}'.format(一逝['內容'], 錯誤)
            )
        if 一逝['開始時間'] < 0.0:
            raise ValidationError(
                '「{}」的開始時間「{}」是負的'.format(一逝, 一逝['開始時間'])
            )
        if 一逝['開始時間'] >= 一逝['結束時間']:
            raise ValidationError(
                '開始時間「{}」無較細結束時間「{}」'.format(一逝['開始時間'], 一逝['結束時間'])
            )


def 檢查聽拍結束時間有超過音檔無(音檔長度, 聽拍):
    for 一逝 in 聽拍:
        try:
            if 一逝['結束時間'] > 音檔長度:
                raise ValidationError(
                    '結束時間「{}」超過音檔長度「{}」'.format(一逝['結束時間'], 音檔長度)
                )
        except KeyError:
            raise ValidationError(
                '聽拍語句「{}」無結束時間'.format(一逝)
            )
        except TypeError:
            raise ValidationError(
                '聽拍「{}」毋是陣列'.format(聽拍)
            )
