from django.test.testcases import TestCase
from 臺灣言語服務.漢語語音處理 import 漢語語音處理


class 切漢語韻試驗(TestCase):

    def test_孤母音(self):
        self.assertEqual(漢語語音處理.切漢語韻('e'), ['e', ])

    def test_雙母音(self):
        self.assertEqual(漢語語音處理.切漢語韻('au'), ['a', 'u', ])

    def test_入聲(self):
        self.assertEqual(漢語語音處理.切漢語韻('iap'), ['i', 'a', 'p', ])

    def test_鼻音(self):
        self.assertEqual(漢語語音處理.切漢語韻('eⁿ'), ['eⁿ', ])

    def test_雙鼻音(self):
        self.assertEqual(漢語語音處理.切漢語韻('aⁿuⁿ'), ['aⁿ', 'uⁿ'])

    def test_鼻音入聲(self):
        self.assertEqual(漢語語音處理.切漢語韻('aⁿuⁿʔ'), ['aⁿ', 'uⁿ', 'ʔ'])

    def test_陽聲韻(self):
        self.assertEqual(漢語語音處理.切漢語韻('iam'), ['i', 'a', 'm', ])

    def test_鼻化韻(self):
        self.assertEqual(漢語語音處理.切漢語韻('m̩'), ['m̩', ])

    def test_鼻化入聲韻(self):
        self.assertEqual(漢語語音處理.切漢語韻('ŋ̩ʔ'), ['ŋ̩', 'ʔ', ])
