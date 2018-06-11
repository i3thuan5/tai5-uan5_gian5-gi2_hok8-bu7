

from 臺灣言語服務.Moses模型訓練 import Moses模型訓練
from 臺灣言語服務.management.commands.訓練Moses import Command as 訓練Moses
from 臺灣言語服務.資料模型路徑 import 翻譯正規化模型資料夾


class Command(訓練Moses):
    def 翻譯做資料夾(self):
        return 翻譯正規化模型資料夾

    def 訓練做(self):
        return Moses模型訓練.訓練正規化模型
