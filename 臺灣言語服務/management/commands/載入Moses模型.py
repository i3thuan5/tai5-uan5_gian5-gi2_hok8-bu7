from django.core.management.base import BaseCommand
from 臺灣言語服務.模型訓練 import 模型訓練
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾
from 臺灣言語服務.資料模型路徑 import 翻譯模型資料夾
from 臺灣言語服務.模型載入 import 模型載入


class Command(BaseCommand):
    help = '載入摩西翻譯模型'

    def handle(self, *args, **參數):
        摩西模型=模型載入.摩西模型()
        
