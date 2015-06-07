# -*- coding: utf-8 -*-
import os
from shutil import rmtree
from unittest.case import TestCase


from 臺灣言語工具.翻譯.摩西工具.摩西翻譯模型訓練 import 摩西翻譯模型訓練
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器
from 臺灣言語工具.翻譯.摩西工具.斷詞轉斷字的編碼器 import 斷詞轉斷字編碼器
from 臺灣言語工具.翻譯.摩西工具.摩西服務端 import 摩西服務端
from 臺灣言語工具.翻譯.摩西工具.摩西用戶端 import 摩西用戶端
from 臺灣言語工具.斷詞.中研院.斷詞用戶端 import 斷詞用戶端
from 臺灣言語工具.翻譯.斷詞斷字翻譯 import 斷詞斷字翻譯
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from time import sleep

if __name__ == '__main__':
	這馬目錄 = os.path.dirname(os.path.abspath(__file__))
	moses模型資料夾路徑 = os.path.join(這馬目錄,'模型訓練', '翻譯模型')
	服務 = 摩西服務端(moses模型資料夾路徑, 埠=8500)
	服務.走()
	while True:
		pass
