# -*- coding: utf-8 -*-
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.語音合成.語音標仔轉換 import 語音標仔轉換
import Pyro4
from 臺灣言語服務.HTS載入 import HTS載入


@Pyro4.expose
class HTS服務:

    def __init__(self):
        self.全部合成母語模型 = HTS載入.HTS模型()

    @Pyro4.expose
    def 支援腔口(self):
        return sorted(self.全部合成母語模型.keys())

    @Pyro4.expose
    def 語音合成實作(self, 查詢腔口, 查詢語句):
        合成母語模型 = self.全部合成母語模型[查詢腔口]
        母語章物件 = (
            拆文分析器.分詞章物件(查詢語句)
            .轉音(合成母語模型['拼音'], 函式='音值')
        )
        try:
            音值物件 = 母語章物件.做(合成母語模型['變調'], '變調')
        except:
            音值物件 = 母語章物件
        標仔陣列 = 語音標仔轉換.物件轉完整合成標仔(音值物件)
        愛合成標仔 = 語音標仔轉換.跳脫標仔陣列(標仔陣列)
        if 愛合成標仔 == []:
            愛合成標仔.append(語音標仔轉換.恬標仔())
        return 合成母語模型['模型'].合成(愛合成標仔).wav格式資料()
