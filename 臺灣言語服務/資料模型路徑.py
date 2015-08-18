from django.conf import settings
from os.path import join


try:
    資料模型路徑 = settings.臺灣言語服務資料模型路徑
except AttributeError:
    資料模型路徑 = join(settings.BASE_DIR, '資料')

翻譯語料資料夾 = join(資料模型路徑, '翻譯語料')
翻譯模型資料夾 = join(資料模型路徑, '翻譯模型')
合成模型資料夾 = join(資料模型路徑, '合成模型')