from django.test.testcases import TestCase


class 閩南語羅馬字轉換整合試驗(TestCase):
    # 輸入可以是漢羅、全羅
    # 羅馬字可以是臺羅傳統調、白話字傳統調、臺羅數字調、白話字數字調

    def test_輸出轉換臺羅(self):
        回應物件 = self.取得羅馬字轉換物件('Tāiⁿ')
        self.assertEqual(
            回應物件['臺羅'],
            'Tāinn'
        )

    def test_輸出轉換白話字(self):
        回應物件 = self.取得羅馬字轉換物件('Tāinn')
        self.assertEqual(
            回應物件['白話字'],
            'Tāiⁿ'
        )

    def test_不轉換漢字(self):
        回應物件 = self.取得羅馬字轉換物件('媠媠e5姑娘')
        self.assertEqual(
            回應物件['白話字'],
            '媠媠ê姑娘'
        )

    def test_保留空白(self):
        回應物件 = self.取得羅馬字轉換物件('Li2 --honnh4')
        self.assertEqual(
            回應物件['白話字'],
            'Lí --hoⁿh'
        )

    def test_保留換行(self):
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢腔口': '閩南語',
                '查詢語句': 'Guá\n--honnh',
            }
        )
        回應物件 = self.取得羅馬字轉換物件('Guá\n--honnh')
        self.assertEqual(
            回應物件['臺羅'],
            'Guá\n--honnh'
        )

    def test_保留漢羅的連字符(self):
        回應物件 = self.取得羅馬字轉換物件('定-tio̍h')
        self.assertEqual(
            回應物件['白話字'],
            '定-tio̍h'
        )

    def test_保留漢羅的輕聲符(self):
        回應物件 = self.取得羅馬字轉換物件('定--tio̍h')
        self.assertEqual(
            回應物件['白話字'],
            '定--tio̍h'
        )

    def test_保留大小寫(self):
        回應物件 = self.取得羅馬字轉換物件('lí Lí')
        self.assertEqual(
            回應物件['臺羅'],
            'lí Lí'
        )

    def test_不轉換非法的拼音(self):
        回應物件 = self.取得羅馬字轉換物件('g0v')
        self.assertEqual(
            回應物件['臺羅'],
            'g0v'
        )

    def 取得羅馬字轉換物件(self, 查詢語句):
        # 預設只查詢閩南語，所以不加查詢腔口
        連線回應 = self.client.get(
            '/羅馬字轉換',
            {
                '查詢語句': 查詢語句,
            }
        )
        轉換物件 = 連線回應.json()
        return 轉換物件
