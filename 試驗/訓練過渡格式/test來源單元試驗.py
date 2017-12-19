# -*- coding: utf-8 -*-
from django.test import TestCase
import json


class 加來源試驗(TestCase):

    def test_有來源(self):
        self.fail()

    def test_一定愛有來源(self):
        self.fail()
        self.assertRaises(
            KeyError, 來源表.加來源, {'姓名': 'Dr. Pigu', '出世年': '1990', })
