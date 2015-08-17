# -*- coding: utf-8 -*-
from django.conf import settings
import os
'''
from 臺灣言語服務.摩西服務 import 摩西服務
摩西服務()
'''

from 臺灣言語工具.翻譯.摩西工具.摩西服務端 import 摩西服務端

def 摩西服務():
    moses模型資料夾路徑 = os.path.join(settings.BASE_DIR, '語料', '翻譯模型','閩南語')
    服務 = 摩西服務端(moses模型資料夾路徑, 埠=8500)
    服務.走()
    服務.等()
