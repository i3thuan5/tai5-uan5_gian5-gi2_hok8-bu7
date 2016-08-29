# -*- coding: utf-8 -*-
from django.apps import AppConfig
from 臺灣言語服務.Moses載入 import Moses載入
from 臺灣言語服務.HTS載入 import HTS載入


全部翻譯母語模型 = {}
全部合成母語模型 = {}


class 模型載入(AppConfig):
    name = '臺灣言語服務'
    verbose_name = "臺灣言語服務模型載入"

    def ready(self):
#         try:
#             全部翻譯母語模型 = Moses載入.摩西模型()
#         except FileNotFoundError:
#             pass
        print('XD')
        try:
            全部合成母語模型 = HTS載入.HTS模型()
            print('xx',全部合成母語模型)
        except FileNotFoundError:
            raise
            pass
