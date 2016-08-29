from django.conf import settings
from os.path import join


try:
    資料路徑 = settings.臺灣言語服務資料路徑
except AttributeError:
    資料路徑 = join(settings.BASE_DIR, '服務資料')

翻譯語料資料夾 = lambda 語言: join(資料路徑, 語言, '翻譯語料')
翻譯模型資料夾 = lambda 語言: join(資料路徑, 語言, '翻譯模型')
合成模型資料夾 = lambda 語言: join(資料路徑, 語言, '合成模型')
合成模型路徑 = lambda 語言: join(語言, 合成模型資料夾(語言), 'Taiwanese.htsvoice')
