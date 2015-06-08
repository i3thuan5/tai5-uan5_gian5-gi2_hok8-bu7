# -*- coding: utf-8 -*-
import os

from 臺灣言語工具.翻譯.摩西工具.摩西服務端 import 摩西服務端

if __name__ == '__main__':
	這馬目錄 = os.path.dirname(os.path.abspath(__file__))
	moses模型資料夾路徑 = os.path.join(這馬目錄, '模型訓練', '翻譯模型')
	服務 = 摩西服務端(moses模型資料夾路徑, 埠=8500)
	服務.走()
	服務.等()
