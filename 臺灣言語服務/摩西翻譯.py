# -*- coding: utf-8 -*-
import os

from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器
from 臺灣言語工具.翻譯.摩西工具.摩西用戶端 import 摩西用戶端
from 臺灣言語工具.斷詞.中研院.斷詞用戶端 import 斷詞用戶端
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from django.http.response import HttpResponse

class 摩西翻譯():
	def __init__(self):
		self.這馬目錄 = os.path.dirname(os.path.abspath(__file__))
		self.moses模型資料夾路徑 = os.path.join(self.這馬目錄, '模型語料', '翻譯模型')
	def 翻譯(self, request, 查詢腔口, 查詢語句):
		翻譯編碼器 = 語句編碼器()
		
		分析器 = 拆文分析器()
		華語章物件 = 分析器.轉做章物件(查詢語句)
		
		斷詞用戶 = 斷詞用戶端()
		華語斷詞章物件 = 斷詞用戶.斷詞(華語章物件)
		
		摩西用戶 = 摩西用戶端(埠=8500, 編碼器=翻譯編碼器)
		閩南語章物件, _翻譯結構華語章物件, _分數 = 摩西用戶.翻譯(華語斷詞章物件)
		
		譀鏡 = 物件譀鏡()
		return HttpResponse(譀鏡.看型(閩南語章物件).encode('utf-8'))
		
if __name__ == '__main__':
	摩西翻譯().翻譯()
