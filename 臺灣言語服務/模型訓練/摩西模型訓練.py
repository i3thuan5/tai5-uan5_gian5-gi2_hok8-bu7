# -*- coding: utf-8 -*-
import os


from 臺灣言語工具.翻譯.摩西工具.摩西翻譯模型訓練 import 摩西翻譯模型訓練
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器

class 摩西模型訓練():
	def __init__(self):
		self.這馬目錄 = os.path.dirname(os.path.abspath(__file__))
		資料目錄 = os.path.join(self.這馬目錄, '翻譯語料')
		self.平行華語 = [os.path.join(資料目錄, '華.gz'), ]
		self.平行閩南語 = [os.path.join(資料目錄, '閩.gz'), ]
		self.閩南語語料 = [os.path.join(資料目錄, '閩.gz'), ]
		self.moses模型資料夾路徑 = os.path.join(self.這馬目錄, '翻譯模型')
	def 單一模型訓練(self):
		翻譯編碼器 = 語句編碼器()  # 若用著Unicdoe擴充就需要
		
		模型訓練 = 摩西翻譯模型訓練()
		模型訓練.訓練(
				self.平行華語, self.平行閩南語, self.閩南語語料,
				self.moses模型資料夾路徑,
				連紲詞長度=2,
				編碼器=翻譯編碼器,
				刣掉暫存檔=True,
			)
		
if __name__ == '__main__':
	摩西模型訓練().單一模型訓練()