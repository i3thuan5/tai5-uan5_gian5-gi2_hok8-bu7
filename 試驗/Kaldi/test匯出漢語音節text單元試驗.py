from os.path import join, isdir
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.core.management import call_command
from django.test.testcases import TestCase


from 臺灣言語服務.Kaldi語料處理 import Kaldi語料處理
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本
from os import makedirs


class 匯出漢語音節text單元試驗(TestCase):

    def test_轉音節(self):
        音節 = Kaldi語料處理.轉音節text格式(
            臺灣閩南語羅馬字拼音,
            [
                'tong0000000-0000000無註明-ku0000000 '
                '敢-若｜kan2-na2 散-步｜san3-poo7 咧｜leh4'
            ]
        )
        self.assertEqual(
            音節,
            [
                'tong0000000-0000000無註明-ku0000000 '
                'kan na san poo leh'
            ]
        )

    def test_標點無要緊(self):
        音節 = Kaldi語料處理.轉音節text格式(
            臺灣閩南語羅馬字拼音,
            [
                'tong0000000-0000000無註明-ku0000000 '
                '敢-若｜kan2-na2 散-步｜san3-poo7 咧｜咧 !｜!'
            ]
        )
        self.assertEqual(
            音節,
            [
                'tong0000000-0000000無註明-ku0000000 '
                'kan na san poo'
            ]
        )

    def test_無講話無要緊(self):
        音節 = Kaldi語料處理.轉音節text格式(
            臺灣閩南語羅馬字拼音,
            [
                'tong0000000-0000000無註明-ku0000000'
            ]
        )
        self.assertEqual(
            音節,
            [
                'tong0000000-0000000無註明-ku0000000'
            ]
        )

    def test_有空逝無要緊(self):
        音節 = Kaldi語料處理.轉音節text格式(
            臺灣閩南語羅馬字拼音,
            [
                'tong0000000-0000000無註明-ku0000000 '
                '敢-若｜kan2-na2 散-步｜san3-poo7 咧｜咧 !｜!',
                ''
            ]
        )
        self.assertEqual(
            音節,
            [
                'tong0000000-0000000無註明-ku0000000 '
                'kan na san poo'
            ]
        )

    @patch('臺灣言語服務.Kaldi語料處理.Kaldi語料處理.轉音節text格式')
    def test_指令有輸出辭典檔(self, 轉音節text格式mock):
        轉音節text格式mock.return_value = [
            'tong0000000-0000000無註明-ku0000000 '
            'kan na san poo leh'
        ]
        with TemporaryDirectory() as 資料夾路徑:
            原本語料 = join(資料夾路徑, 'train_dev')
            makedirs(原本語料)
            with open(join(原本語料, 'text'), 'w') as 檔案:
                print(
                    'tong0000000-0000000無註明-ku0000000 '
                    '敢-若｜kan2-na2 散-步｜san3-poo7 咧｜leh4',
                    file=檔案
                )
            結果語料 = join(資料夾路徑, 'train_dev_free')

            call_command('轉Kaldi音節text', '台語', 原本語料, 結果語料)

            self.assertEqual(
                程式腳本._讀檔案(join(結果語料, 'text')),
                [
                    'tong0000000-0000000無註明-ku0000000 '
                    'kan na san poo leh'
                ]
            )

    def test_有khok4pi3檔案(self):
        with TemporaryDirectory() as 資料夾路徑:
            原本語料 = join(資料夾路徑, 'train_dev')
            makedirs(原本語料)
            程式腳本._字串寫入檔案(
                join(原本語料, 'text'),
                'tong0000000-0000000無註明-ku0000000 '
                '敢-若｜kan2-na2 散-步｜san3-poo7 咧｜leh4'
            )
            程式腳本._字串寫入檔案(join(原本語料, 'utt2spk'), 'kiann5')
            結果語料 = join(資料夾路徑, 'train_dev_free')

            call_command('轉Kaldi音節text', '台語', 原本語料, 結果語料)

            self.assertEqual(
                程式腳本._讀檔案(join(結果語料, 'utt2spk')),
                程式腳本._讀檔案(join(原本語料, 'utt2spk'))
            )

    def test_split資料夾愛thai5掉(self):
        with TemporaryDirectory() as 資料夾路徑:
            原本語料 = join(資料夾路徑, 'train_dev')
            makedirs(原本語料)
            程式腳本._字串寫入檔案(
                join(原本語料, 'text'),
                'tong0000000-0000000無註明-ku0000000 '
                '敢-若｜kan2-na2 散-步｜san3-poo7 咧｜leh4'
            )
            結果語料 = join(資料夾路徑, 'train_dev_free')
            split16 = join(結果語料, 'split16')
            makedirs(split16)

            call_command('轉Kaldi音節text', '台語', 原本語料, 結果語料)

            self.assertFalse(isdir(split16))
