from django.test.testcases import TestCase


class 閩南語羅馬字轉換整合試驗(TestCase):
    # 輸入可以是漢羅、全羅
    # 羅馬字可以是臺羅傳統調、白話字傳統調、臺羅數字調、白話字數字調

    def test_輸出轉換臺羅(self):
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

    def test_輸出轉換白話字(self):
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
                '查詢語句': '媠媠e5姑娘',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['白話字'],
            '媠媠ê姑娘'
        )

    def test_保留空白(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '查詢語句': 'Li2 --ah4 --honnh4,',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['白話字'],
            'Lí --ah --hoⁿh,'
        )
    
    def test_保留漢羅的連字符(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '查詢語句': '定-tio̍h',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['白話字'],
            '定-tio̍h'
        )
    
    def test_保留漢羅的輕聲符(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '查詢語句': '定--tio̍h',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['白話字'],
            '定--tio̍h'
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

    def test_逗號後壁小寫(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '查詢語句': 'Guá, guá',
            }
        )
        回應物件 = 連線回應.json()
        self.assertEqual(
            回應物件['多元書寫'][0]['臺羅'],
            'Guá,'
        )
        self.assertEqual(
            回應物件['多元書寫'][1]['臺羅'],
            'guá'
        )

    def test_換行斷開(self):
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
    