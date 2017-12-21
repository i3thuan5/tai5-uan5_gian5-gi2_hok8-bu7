from os.path import join
from tempfile import TemporaryDirectory

from django.db.models.query_utils import Q
from django.test.testcases import TestCase


from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.models import 訓練過渡格式


class Kaldi匯出一種語言語料單元試驗(TestCase):

    def test_一條一句(self):
        self.匯入音檔('媠巧',     'tsiang5 tsiang5')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語',臺灣閩南語羅馬字拼音,
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'text'),
                ['0000000媠巧-tong0000000-ku0000000 tsiang5 tsiang5']
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'wav.scp'),
                'sox'
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'segments'),
                '0000000媠巧-tong0000000-ku0000000'
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'reco2file_and_channel'),
                'tong0000000'
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                ['0000000媠巧-tong0000000-ku0000000 0000000媠巧']
            )

    def test_兩句一條(self):
        self.匯入音檔(
            '媠巧',
            'tsiang5 tsiang5',
        )
        self.匯入音檔(
            '豬仔',
            'konn5 konn5',
        )
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語',臺灣閩南語羅馬字拼音,
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'text'),
                [
                    '0000000媠巧-tong0000000-ku0000000 tsiang5 tsiang5',
                    '0000001豬仔-tong0000001-ku0000000 konn5 konn5',
                ]
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'wav.scp'),
                'sox'
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'segments'),
                '0000000媠巧-tong0000000-ku0000000'
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'segments'),
                '0000001豬仔-tong0000001-ku0000000'
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'reco2file_and_channel'),
                'tong0000000'
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'reco2file_and_channel'),
                'tong0000001'
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                [
                    '0000000媠巧-tong0000000-ku0000000 0000000媠巧',
                    '0000001豬仔-tong0000001-ku0000000 0000001豬仔',
                ]
            )

    def test_一條兩句(self):
        一筆 = self.匯入音檔('媠巧', 'sui2')
        一筆.聽拍 = [
            {
                '語者': '媠巧',
                '內容': 'tsiang5 tsiang5',
                '開始時間': 0.3,
                '結束時間': 1,
            },
            {
                '語者': '豬仔',
                '內容': 'konn5 konn5',
                '開始時間': 2,
                '結束時間': 3,
            },
        ]
        一筆.save()
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語',臺灣閩南語羅馬字拼音,
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'text'),
                [
                    '0000000媠巧-tong0000000-ku0000000 tsiang5 tsiang5',
                    '0000001豬仔-tong0000000-ku0000001 konn5 konn5',
                ]
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'wav.scp'),
                'sox'
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'segments'),
                '0000000媠巧-tong0000000-ku0000000'
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'segments'),
                '0000001豬仔-tong0000000-ku0000001'
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'reco2file_and_channel'),
                'tong0000000'
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                [
                    '0000000媠巧-tong0000000-ku0000000 0000000媠巧',
                    '0000001豬仔-tong0000000-ku0000001 0000001豬仔',
                ]
            )

    def test_仝名愛當作仝人(self):
        self.匯入音檔('媠巧', 'tsiang5 tsiang5')
        self.匯入音檔('媠巧', 'konn5 konn5')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語',臺灣閩南語羅馬字拼音,
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'text'),
                [
                    '0000000媠巧-tong0000000-ku0000000 tsiang5 tsiang5',
                    '0000000媠巧-tong0000001-ku0000000 konn5 konn5',
                ]
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                [
                    '0000000媠巧-tong0000000-ku0000000 0000000媠巧',
                    '0000000媠巧-tong0000001-ku0000000 0000000媠巧',
                ]
            )

    def test_無註明愛當作無仝人(self):
        self.匯入音檔('無註明', 'tsiang5 tsiang5')
        self.匯入音檔('無註明', 'konn5 konn5')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語',臺灣閩南語羅馬字拼音,
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'text'),
                [
                    '0000000無註明-tong0000000-ku0000000 tsiang5 tsiang5',
                    '0000001無註明-tong0000001-ku0000000 konn5 konn5',
                ]
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                [
                    '0000000無註明-tong0000000-ku0000000 0000000無註明',
                    '0000001無註明-tong0000001-ku0000000 0000001無註明',
                ]
            )

    def test_輸出一句(self):
        self.匯入音檔('konn5', 'konn5 konn5')
        一筆 = self.匯入音檔('媠巧', 'tsiang5 tsiang5')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語',臺灣閩南語羅馬字拼音,
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料(),
                Q(pk=一筆.編號())
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'text'),
                ['0000000媠巧-tong0000000-ku0000000 tsiang5 tsiang5']
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'wav.scp'),
                'sox'
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'segments'),
                '0000000媠巧-tong0000000-ku0000000'
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'reco2file_and_channel'),
                'tong0000000'
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                ['0000000媠巧-tong0000000-ku0000000 0000000媠巧']
            )

    def test_一條內底有換逝(self):
        self.匯入音檔('媠巧', '\ntsiang5\ntsiang5\n')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語',臺灣閩南語羅馬字拼音,
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'text'),
                ['0000000媠巧-tong0000000-ku0000000 tsiang5 tsiang5']
            )

    def 匯入音檔(self, 語者, 內容):
        with TemporaryDirectory() as 資料夾路徑:
            音檔所在 = join(資料夾路徑, 'siann.wav')
            with open(音檔所在, 'wb') as 檔案:
                檔案.write(聲音檔.對參數轉(2, 16, 1, b'sui2khiau2' * 160).wav格式資料())
            return 訓練過渡格式.objects.create(
                來源='媠巧',
                年代='2017',
                種類='語句',
                影音所在=音檔所在,
                影音語者=語者,
                文本=內容,
            )

    def 比較檔案(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertEqual(檔案.read(), '\n'.join(資料) + '\n')

    def 檔案內底有(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertIn(資料, 檔案.read())
