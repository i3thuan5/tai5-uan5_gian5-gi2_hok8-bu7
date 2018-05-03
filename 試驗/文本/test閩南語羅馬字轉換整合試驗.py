from django.test.testcases import TestCase


class 閩南語羅馬字轉換整合試驗(TestCase):
    def test_臺羅轉換臺羅(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '查詢語句': 'Lí tāinn-tio̍h',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['臺羅'],
            'Lí tāinn-tio̍h'
        )

    def test_臺羅轉換白話字(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '查詢語句': 'Lí tāinn-tio̍h',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['白話字'],
            'Lí tāiⁿ-tio̍h'
        )

    def test_不轉換漢字(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '查詢語句': '媠媠的姑娘',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['臺羅'],
            '媠媠的姑娘'
        )

    def test_保留使用者的斷詞方式(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '查詢語句': 'Lí --ah --honnh,',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['白話字'],
            'Lí --ah --hoⁿh,'
        )

    def test_頭字大寫(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '查詢語句': 'lí',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['臺羅'], 
            'Lí'
        )

    def test_多句轉換(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '查詢語句': 'Guá\n--honnh',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['臺羅'],
            'Guá'
        )
        self.assertEqual(
            回應物件['多元書寫'][1]['臺羅'],
            '--Honnh'
        )
    
    def test_逗號後壁小寫(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '查詢語句': 'Guá,guá',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['臺羅'],
            'Guá'
        )
        self.assertEqual(
            回應物件['多元書寫'][1]['臺羅'],
            'guá'
        )