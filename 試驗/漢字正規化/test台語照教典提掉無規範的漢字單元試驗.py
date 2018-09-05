# -*- coding: utf-8 -*-
import io
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase


from 臺灣言語服務.過渡語料 import 過渡語料處理
from django.core.management.base import CommandError


class test單元試驗(TestCase):
    pass