from django.test.testcases import TestCase


class 閩南語羅馬字轉換整合試驗(TestCase):
    def test_臺羅轉換臺羅(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '字': 'Lí tāinn-tio̍h sī jiá lāu-su siū-khì --ah --honnh,',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['臺羅'],
            'Lí tāinn-tio̍h sī jiá lāu-su siū-khì --ah --honnh,'
        )

    def test_臺羅轉換白話字(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '查詢語句': 'Lí tāinn-tio̍h sī jiá lāu-su siū-khì --ah --honnh,',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['白話字'],
            'Lí tāiⁿ-tio̍h sī jiá lāu-su siū-khì --ah --hoⁿh,'
        )

    def test_不轉換漢字(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '字': '媠媠的姑娘',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['臺羅'],
            '媠媠的姑娘'
        )

    def test_多句轉換(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '字': 'gua2,tāinn-tio̍h\n--honnh',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['白話字'],
            'góa'
        )
        self.assertEqual(
            回應物件['多元書寫'][1]['白話字'],
            'tāiⁿ-tio̍h'
        )
        self.assertEqual(
            回應物件['多元書寫'][2]['白話字'],
            '--honnⁿh'
        )
        
        