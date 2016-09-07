from django.conf import settings
from os.path import join


try:
    資料路徑 = settings.臺灣言語服務資料路徑
except AttributeError:
    資料路徑 = join(settings.BASE_DIR, '服務資料')


def 翻譯語料資料夾(語言):
    return join(資料路徑, 語言, '翻譯語料')


def 翻譯模型資料夾(語言):
    return join(資料路徑, 語言, '翻譯模型')


def 合成模型資料夾(語言):
    return join(資料路徑, 語言, '合成模型')


def 合成模型路徑(語言):
    return join(語言, 合成模型資料夾(語言), 'Taiwanese.htsvoice')
