from django.test.testcases import TestCase


class 閩南語對齊整合試驗(TestCase):

    def test_分詞愛數字調(self):
        連線要求 = self.client.get(
            '/漢字音標對齊',
            {
                '查詢腔口': '閩南語',
                '漢字': '媠媠的姑娘',
                '音標': 'sui2--Sui2 E5 koo-niû',
            }
        )
        回應物件 = 連線要求.json()
        self.assertEqual(
            回應物件['分詞'],
            '媠｜sui2 媠｜0sui2 的｜e5 姑-娘｜koo1-niu5'
        )

    def test_閏號保持大小寫(self):
        連線要求 = self.client.get(
            '/漢字音標對齊',
            {
                '查詢腔口': '閩南語',
                '漢字': '媠媠的姑娘',
                '音標': 'sui2--Sui2 E5 koo-niû',
            }
        )
        回應物件 = 連線要求.json()
        self.assertEqual(
            回應物件['音標'],
            'suí--Suí Ê koo-niû'
        )

    def test_漢字照詞分開(self):
        連線要求 = self.client.get(
            '/漢字音標對齊',
            {
                '查詢腔口': '閩南語',
                '漢字': '媠媠的姑娘',
                '音標': 'sui2--Sui2 E5 koo-niû',
            }
        )
        回應物件 = 連線要求.json()
        self.assertEqual(
            回應物件['漢字'],
            '媠 媠 的 姑娘'
        )

    def test_漢語濫英語(self):
        連線要求 = self.client.get(
            '/漢字音標對齊',
            {
                '查詢腔口': '閩南語',
                '漢字': '伊干焦知影印尼來的外勞『Wati』爾爾。',
                '音標': 'I kan-na tsai-iánn Ìn-nî lâi ê guā-lô ‘Wati’ niā-niā.',
            }
        )
        回應物件 = 連線要求.json()
        self.assertIn('分詞', 回應物件)

    def test_臺語濫華語(self):
        連線要求 = self.client.get(
            '/漢字音標對齊',
            {
                '查詢腔口': '閩南語',
                '漢字': '是華語叫做『陀螺』的「干樂」。',
                '音標': 'sī huâ-gí kiò-tsò “陀螺” ê “kan-lo̍k”.',
            }
        )
        回應物件 = 連線要求.json()
        self.assertIn('分詞', 回應物件)
