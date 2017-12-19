from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
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
