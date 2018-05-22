
from 臺灣言語服務.Moses模型訓練 import Moses模型訓練
from 臺灣言語服務.資料模型路徑 import 翻譯做外文模型資料夾
from 臺灣言語服務.management.commands.訓練Moses import Command as 訓練Moses


class Command(訓練Moses):
    翻譯做資料夾 = 翻譯做外文模型資料夾
    訓練做 = Moses模型訓練.訓練翻譯做外文模型
