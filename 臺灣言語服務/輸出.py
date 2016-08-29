import gzip
from os import makedirs
from os.path import join

from django.db.models.query_utils import Q


from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.欄位資訊 import 語句
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語服務.資料模型路徑 import 翻譯語料資料夾


class 資料輸出工具:
    翻譯語料檔名 = [
        '對齊外語語句',
        '對齊母語語句',
        '語句文本',
        '對齊外語字詞',
        '對齊母語字詞',
        '字詞文本',
    ]
    文本語料檔名 = [
        '語句文本',
        '字詞文本',
    ]

    def __init__(self, 要求語言=None):
        if 要求語言 is None:
            self.條件 = Q()
            self.腔口條件 = Q()
        else:
            self.條件 = Q(語言腔口__語言腔口=要求語言)
            self.腔口條件 = Q(語言腔口=要求語言)

    def 輸出翻譯語料(self):
        檔案表 = self._建立檔案表(
            語言腔口表.揣出有語句文本的語言腔口().filter(self.腔口條件), self.翻譯語料檔名
        )
        for 外語 in 外語表.全部外語資料().filter(self.條件):
            try:
                檔案表欄位 = 檔案表[外語.語言腔口.語言腔口][外語.種類.種類]
            except KeyError:
                pass
            else:
                self._加文本翻譯語料(
                    檔案表欄位, [外語.外語資料], 外語.翻譯文本, '文本'
                )
                for 影音關係 in 外語.翻譯影音.all():
                    影音 = 影音關係.影音
                    self._加文本翻譯語料(
                        檔案表欄位, [外語.外語資料], 影音.影音文本, '文本'
                    )

        for 影音 in 影音表.源頭的影音資料().filter(self.條件):
            try:
                檔案表欄位 = 檔案表[影音.語言腔口.語言腔口][影音.種類.種類]
            except KeyError:
                pass
            else:
                self._加文本翻譯語料(
                    檔案表欄位, [], 影音.影音文本, '文本'
                )
        for 文本 in 文本表.源頭的文本資料().filter(self.條件):
            try:
                檔案表欄位 = 檔案表[文本.語言腔口.語言腔口][文本.種類.種類]
            except KeyError:
                pass
            else:
                文本格式化資料 = 文本.文本佮音標格式化資料()
                if 文本.文本校對.exists():
                    self._加文本翻譯語料(
                        檔案表欄位, [文本格式化資料], 文本.文本校對, '新文本'
                    )
                else:
                    print(文本格式化資料, file=檔案表欄位['對齊外語'])
                    print(文本格式化資料, file=檔案表欄位['對齊母語'])
                    print(文本格式化資料, file=檔案表欄位['文本'])
        self._關檔案表的檔案(檔案表)

    def 輸出文本語料(self):
        檔案表 = self._建立檔案表(
            語言腔口表.揣出有文本的語言腔口().filter(self.腔口條件), self.文本語料檔名
        )
        for 文本 in 文本表.上尾層的文本資料().filter(self.條件):
            檔案表欄位 = 檔案表[文本.語言腔口.語言腔口][文本.種類.種類]
            print(文本.文本佮音標格式化資料(), file=檔案表欄位['文本'])
        self._關檔案表的檔案(檔案表)

    def _建立檔案表(self, 腔口, 語料檔名):
        檔案表 = {}
        for 腔 in 腔口:
            makedirs(翻譯語料資料夾(腔.語言腔口), exist_ok=True)
            檔案表[腔.語言腔口] = {語句: {}, 字詞: {}}
            for 檔名 in self.翻譯語料檔名:
                if 語句 in 檔名:
                    檔案表[腔.語言腔口][語句][檔名.replace(語句, '')] = gzip.open(
                        join(翻譯語料資料夾(腔.語言腔口), 檔名 + '.txt.gz'), 'wt')
                else:
                    檔案表[腔.語言腔口][字詞][檔名.replace(字詞, '')] = gzip.open(
                        join(翻譯語料資料夾(腔.語言腔口), 檔名 + '.txt.gz'), 'wt')
        return 檔案表

    def _關檔案表的檔案(self, 檔案表):
        for 腔檔案 in 檔案表.values():
            for 種類內檔案 in 腔檔案.values():
                for 一个檔案 in 種類內檔案.values():
                    一个檔案.close()

    def _加文本翻譯語料(self, 檔案表, 目前資料, 關係表, 文本物件名):
        for 文本關係 in 關係表.all():
            文本 = getattr(文本關係, 文本物件名)
            文本格式化資料 = 文本.文本佮音標格式化資料()
            目前資料.append(文本格式化資料)
            if 文本.文本校對.exists():
                self._加文本翻譯語料(檔案表, 目前資料, 文本.文本校對, '新文本')
            else:
                print('\n'.join(目前資料), file=檔案表['對齊外語'])
                for _ in 目前資料:
                    print(文本格式化資料, file=檔案表['對齊母語'])
                print(文本格式化資料, file=檔案表['文本'])
            目前資料.pop()
