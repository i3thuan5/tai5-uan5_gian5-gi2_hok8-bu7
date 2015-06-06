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

class 摩西翻譯():
	def __init__(self):
		self.這馬目錄 = os.path.dirname(os.path.abspath(__file__))
		self.moses模型資料夾路徑 = os.path.join(self.這馬目錄, '模型語料','翻譯模型')
	def test_單一模型訓練(self):
		翻譯編碼器 = 語句編碼器()  # 若用著Unicdoe擴充就需要
# 		服務 = 摩西服務端(self.moses模型資料夾路徑, 埠=8500)
# 		服務.走()
		
		分析器 = 拆文分析器()
		華語章物件 = 分析器.轉做句物件('屏東 潮州 有人 把水果紙箱  套在 身上 。')
		
		斷詞用戶 = 斷詞用戶端()
		華語斷詞章物件 = 斷詞用戶.斷詞(華語章物件)
		
		摩西用戶 = 摩西用戶端(埠=8500, 編碼器=翻譯編碼器)
		閩南語章物件, 翻譯結構華語章物件, 分數 = 摩西用戶.翻譯(華語斷詞章物件)
		
		譀鏡 = 物件譀鏡()
		譀鏡.看型(閩南語章物件))
		