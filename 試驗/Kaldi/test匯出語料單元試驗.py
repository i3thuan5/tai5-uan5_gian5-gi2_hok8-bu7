from os.path import join
from posix import remove
from tempfile import TemporaryDirectory, NamedTemporaryFile

from django.db.models.query_utils import Q
from django.test.testcases import TestCase


from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.語音辨識.聲音檔 import 聲音檔
from 臺灣言語服務.models import 訓練過渡格式
from 臺灣言語服務.kaldi.lexicon import 辭典輸出


class Kaldi匯出一種語言語料單元試驗(TestCase):
    def setUp(self):
        self.檔案 = NamedTemporaryFile(delete=False)
        self.檔案.write(聲音檔.對參數轉(2, 16, 1, b'sui2khiau2' * 160).wav格式資料())
        self.檔案.close()
        self.檔案2 = NamedTemporaryFile(delete=False)
        self.檔案2.write(聲音檔.對參數轉(2, 16, 1, b'sui2khiau2' * 160).wav格式資料())
        self.檔案2.close()

    def tearDown(self):
        remove(self.檔案.name)

    def test_文本有text(self):
        self.匯入音檔('媠巧', 'tsiang5 tsiang5')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'text'),
                ['0語料庫-0000000媠巧-tong0000000-ku0000000 tsiang5 tsiang5']
            )

    def test_聽拍有text(self):
        一筆 = self.匯入音檔('媠巧', None)
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
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'text'),
                [
                    '0語料庫-0000000媠巧-tong0000000-ku0000000 tsiang5 tsiang5',
                    '0語料庫-0000001豬仔-tong0000001-ku0000000 konn5 konn5',
                ]
            )

    def test_音檔有用sox調聲道Kah頻率(self):
        self.匯入音檔('媠巧', 'tsiang5 tsiang5')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'wav.scp'),
                'sox'
            )

    def test_有segments(self):
        self.匯入音檔('媠巧', 'tsiang5 tsiang5')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'segments'),
                '0語料庫-0000000媠巧-tong0000000-ku0000000'
            )

    def test_有reco(self):
        self.匯入音檔('媠巧', 'tsiang5 tsiang5')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.檔案內底有(
                join(資料夾路徑, '語料資料夾', 'train', 'reco2file_and_channel'),
                '0語料庫-tong0000000'
            )

    def test_一條一句ê語者(self):
        self.匯入音檔('媠巧', 'tsiang5 tsiang5')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                ['0語料庫-0000000媠巧-tong0000000-ku0000000 0000000媠巧']
            )

    def test_kāng檔kāng名就kānglâng(self):
        一筆 = self.匯入音檔('媠巧', None)
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
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                [
                    '0語料庫-0000000媠巧-tong0000000-ku0000000 0語料庫-0000000媠巧',
                    '0語料庫-0000000媠巧-tong0000000-ku0000001 0語料庫-0000000媠巧',
                ]
            )

    def test_kāng檔無kāng名(self):
        一筆 = self.匯入音檔('媠巧', None)
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
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                [
                    '0語料庫-0000000媠巧-tong0000000-ku0000000 0語料庫-0000000媠巧',
                    '0語料庫-0000001豬仔-tong0000000-ku0000001 0語料庫-0000001豬仔',
                ]
            )

    def test_kāng檔無名(self):
        一筆 = self.匯入音檔('媠巧', None)
        一筆.聽拍 = [
            {
                '內容': 'tsiang5 tsiang5',
                '開始時間': 0.3,
                '結束時間': 1,
            },
            {
                '內容': 'konn5 konn5',
                '開始時間': 2,
                '結束時間': 3,
            },
        ]
        一筆.save()
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                [
                    '0語料庫-0000000無註明-tong0000000-ku0000000 0語料庫-0000000無註明',
                    '0語料庫-0000001無註明-tong0000000-ku0000001 0語料庫-0000001無註明',
                ]
            )

    def test_無kāng檔kāng名嘛kānglâng(self):
        self.匯入音檔(
            '媠巧',
            'tsiang5 tsiang5',
        )
        self.匯入音檔(
            '媠巧',
            'konn5 konn5',
        )
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                [
                    '0語料庫-0000000媠巧-tong0000000-ku0000000 0語料庫-0000000媠巧',
                    '0語料庫-0000000媠巧-tong0000001-ku0000000 0語料庫-0000000媠巧',
                ]
            )

    def test_無kāng檔無kāng名(self):
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
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                [
                    '0語料庫-0000000媠巧-tong0000000-ku0000000 0語料庫-0000000媠巧',
                    '0語料庫-0000001豬仔-tong0000001-ku0000000 0語料庫-0000001豬仔',
                ]
            )

    def test_無kāng檔無名(self):
        self.匯入音檔('無註明', 'tsiang5 tsiang5')
        self.匯入音檔('無註明', 'konn5 konn5')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                [
                    '0語料庫-0000000無註明-tong0000000-ku0000000 0語料庫-0000000無註明',
                    '0語料庫-0000001無註明-tong0000001-ku0000000 0語料庫-0000001無註明',
                ]
            )

    def test_無kāng來源就攏無kâng(self):
        self.匯入音檔('媠巧', 'Sui', 'Sui-khoo')
        self.匯入音檔('媠巧', 'Khiau', 'Khiau-khoo')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                [
                    '0Sui-khoo-0000000媠巧-tong0000000-ku0000000 0Sui-khoo-0000000媠巧',
                    '1Khiau-khoo-0000000媠巧-tong0000000-ku0000000 1Khiau-khoo-0000000媠巧',
                ]
            )

    def test_輸出指定一句(self):
        self.匯入音檔('konn5', 'konn5 konn5')
        一筆 = self.匯入音檔('媠巧', 'tsiang5 tsiang5')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料(),
                Q(pk=一筆.編號())
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'utt2spk'),
                ['0語料庫-0000000媠巧-tong0000000-ku0000000 0語料庫-0000000媠巧']
            )

    def test_一條內底有換逝(self):
        self.匯入音檔('媠巧', '\ntsiang5\ntsiang5\n')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            self.比較檔案(
                join(資料夾路徑, '語料資料夾', 'train', 'text'),
                ['0語料庫-0000000媠巧-tong0000000-ku0000000 tsiang5 tsiang5']
            )

    def test_仝音檔_wav愛公家(self):
        self.匯入聽拍(self.檔案, '媠', 'sui2')
        self.匯入聽拍(self.檔案, '巧', 'khiau2')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            with open(join(資料夾路徑, '語料資料夾', 'train', 'wav.scp')) as wavscp:
                self.assertEqual(
                    len(wavscp.read().strip().split('\n')),
                    1
                )

    def test_無仝音檔_wav愛分開(self):
        self.匯入聽拍(self.檔案, '媠', 'sui2')
        self.匯入聽拍(self.檔案2, '巧', 'khiau2')
        with TemporaryDirectory() as 資料夾路徑:
            Kaldi語料匯出.匯出一種語言語料(
                '台語', 辭典輸出(臺灣閩南語羅馬字拼音, '拆做音素'),
                資料夾路徑, '語料資料夾', Kaldi語料匯出.初使化辭典資料()
            )
            with open(join(資料夾路徑, '語料資料夾', 'train', 'wav.scp')) as wavscp:
                self.assertEqual(
                    len(wavscp.read().strip().split('\n')),
                    2
                )

    def 匯入音檔(self, 語者, 內容, 來源='語料庫'):
        return 訓練過渡格式.objects.create(
            來源=來源,
            年代='2017',
            種類='語句',
            影音所在=self.檔案.name,
            影音語者=語者,
            文本=內容,
        )

    def 匯入聽拍(self, 檔案, 語者, 內容):
        return 訓練過渡格式.objects.create(
            來源='語料庫',
            年代='2018',
            種類='語句',
            影音所在=檔案.name,
            影音語者=語者,
            聽拍=[{'語者': 語者, '內容': 內容, '開始時間': 0.0, '結束時間': 1.2}],
        )

    def 比較檔案(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertEqual(檔案.read(), '\n'.join(資料) + '\n')

    def 檔案內底有(self, 檔名, 資料):
        with open(檔名) as 檔案:
            self.assertIn(資料, 檔案.read())
