import json
from unittest.mock import patch

from django.test.client import RequestFactory
from django.test.testcases import TestCase


from 臺灣言語服務.Moses服務 import Moses服務
from 臺灣言語服務.Moses介面 import Moses介面
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.音標系統.閩南語綜合標音 import 閩南語綜合標音


class 閩南語對齊整合試驗(TestCase):

    @classmethod
    def setUpClass(cls):
        super(cls, cls).setUpClass()
        cls.服務 = Moses服務({'閩南語': {
            '語族': '漢語',
            '解析拼音': 臺灣閩南語羅馬字拼音,
            '音標系統': 臺灣閩南語羅馬字拼音,
            '字綜合標音': 閩南語綜合標音,
        }})
        cls.ProxyPatch = patch('Pyro4.Proxy')
        ProxyMock = cls.ProxyPatch.start()
        ProxyMock.return_value = cls.服務

    def setUp(self):
        self.服務功能 = Moses介面()

    def test_一般(self):
        連線要求 = RequestFactory().get('/漢字音標對齊')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '漢字': '我愛佇公媽面頭前跪甲食暗才會使起來。',
            '音標': 'guá ài tī kong-má bīn-thâu-tsîng kuī kah tsia̍h-àm tsiah ē-sái khí--lâi.',
        }
        連線回應 = self.服務功能.漢字音標對齊(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('分詞', 回應物件)
        self.assertIn('綜合標音', 回應物件)

    def test_漢語濫英語(self):
        連線要求 = RequestFactory().get('/漢字音標對齊')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '漢字': '伊干焦知影印尼來的外勞『Wati』爾爾。',
            '音標': 'I kan-na tsai-iánn Ìn-nî lâi ê guā-lô ‘Wati’ niā-niā.',
        }
        連線回應 = self.服務功能.漢字音標對齊(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('分詞', 回應物件)
        self.assertIn('綜合標音', 回應物件)

    def test_臺語濫華語(self):
        連線要求 = RequestFactory().get('/漢字音標對齊')
        連線要求.GET = {
            '查詢腔口': '閩南語',
            '漢字': '是華語叫做『陀螺』的「干樂」。',
            '音標': 'sī huâ-gí kiò-tsò “陀螺” ê “kan-lo̍k”.',
        }
        連線回應 = self.服務功能.漢字音標對齊(連線要求)
        self.assertEqual(連線回應.status_code, 200)
        回應物件 = json.loads(連線回應.content.decode("utf-8"))
        self.assertIn('分詞', 回應物件)
        self.assertIn('綜合標音', 回應物件)
