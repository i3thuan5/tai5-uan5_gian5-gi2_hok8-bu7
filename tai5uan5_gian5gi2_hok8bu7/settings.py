"""
Django settings for tai5uan5_gian5gi2_hok8bu7 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音相容教會羅馬字音標 import 臺灣閩南語羅馬字拼音相容教會羅馬字音標
from 臺灣言語工具.語音合成.閩南語變調 import 閩南語變調
from 臺灣言語工具.語音辨識.文本音值對照表.閩南語文本音值表 import 閩南語文本音值表
from 臺灣言語工具.語音合成.決策樹仔問題.閩南語決策樹仔 import 閩南語決策樹仔
from 臺灣言語工具.音標系統.客話.臺灣客家話拼音 import 臺灣客家話拼音
from 臺灣言語工具.語音辨識.文本音值對照表.客家話文本音值表 import 客家話文本音值表
from 臺灣言語工具.語音合成.決策樹仔問題.客家話決策樹仔 import 客家話決策樹仔


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')!k=!nrd^r_fs7m%=0h16$o!73p55l32o1v=sqiywv&07nm5kw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '臺灣言語資料庫',
    '臺灣言語服務',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tai5uan5_gian5gi2_hok8bu7.urls'

WSGI_APPLICATION = 'tai5uan5_gian5gi2_hok8bu7.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MEDIA_ROOT = os.path.join(BASE_DIR, "資料庫影音檔案")

MIDDLEWARE_CLASSES += (
    'corsheaders.middleware.CorsMiddleware',
)
CORS_ORIGIN_REGEX_WHITELIST = ('^.*$', )
CORS_ALLOW_CREDENTIALS = True

HOK8_BU7_SIAT4_TING7 = {
    '閩南語': {
        '語族': '漢語',
        '音標系統': 臺灣閩南語羅馬字拼音,
        '解析拼音': 臺灣閩南語羅馬字拼音相容教會羅馬字音標,
        '變調規則': 閩南語變調,
        '文本音值表': 閩南語文本音值表,
        '決策樹仔': 閩南語決策樹仔,
    },
    '詔安腔': {
        '語族': '漢語',
        '音標系統': 臺灣客家話拼音,
        '文本音值表': 客家話文本音值表,
        '決策樹仔': 客家話決策樹仔,
    },
}
