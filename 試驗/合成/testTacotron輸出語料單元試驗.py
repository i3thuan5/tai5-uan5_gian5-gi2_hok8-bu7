from os import listdir
from os.path import join

from django.test.testcases import TestCase


from 試驗.合成.test輸出語料單元試驗 import 輸出語料單元試驗
from 臺灣言語服務.tacotron.輸出 import Tacotron模型訓練


class Tacotron輸出語料單元試驗(輸出語料單元試驗):
    模型訓練 = Tacotron模型訓練.輸出LJ格式

    def 確定檔案數量(self, 目錄, 數量):
        with open(join(目錄, 'taioanoe', 'metadata.csv')) as tong:
            if 數量 == 0:
                self.assertEqual(tong.read().rstrip(), '')
            else:
                self.assertEqual(len(tong.read().rstrip().split('\n')), 數量)
            self.assertEqual(
                len(listdir(join(目錄, 'taioanoe', 'wavs'))),
                數量
            )
