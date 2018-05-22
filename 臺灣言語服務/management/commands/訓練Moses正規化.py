

from 臺灣言語服務.Moses模型訓練 import Moses模型訓練
from 臺灣言語工具.翻譯.摩西工具.安裝摩西翻譯佮相關程式 import 安裝摩西翻譯佮相關程式
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾
from 臺灣言語服務.資料模型路徑 import 翻譯做母語模型資料夾
from 臺灣言語服務.management.commands.訓練Moses import Command as 訓練Moses
from 臺灣言語服務.資料模型路徑 import 翻譯正規化模型資料夾


class Command(訓練Moses):
    help = (
        '訓練Moses模型，會當選愛訓練啥物語言抑是全部語言的。\n'
        '裝Moses程式，掠而且編譯，可能愛半點鐘以上'
    )
    翻譯做資料夾 = 翻譯正規化模型資料夾
    訓練做 = Moses模型訓練.訓練正規化模型

    def handle(self, *args, **參數):
        安裝摩西翻譯佮相關程式.安裝gizapp()
        安裝摩西翻譯佮相關程式.安裝moses(編譯CPU數=參數['核心數'])
        語言 = 參數['語言']
        語料資料夾 = 翻譯語料資料夾(語言)
        模型資料夾 = 翻譯做母語模型資料夾(語言)
        Moses模型訓練.輸出全部語料(語料資料夾)
        Moses模型訓練.訓練翻譯做母語模型(語料資料夾, 模型資料夾)
