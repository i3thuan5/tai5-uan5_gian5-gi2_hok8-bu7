from distutils.core import setup
from os import walk
import os
import sys
from 版本 import 版本

# tar無法度下傷長的檔案名，所以愛用zip
# python setup.py sdist --format=zip upload
try:
    # travis攏先`python setup.py sdist`才閣上傳
    sys.argv.insert(sys.argv.index('sdist') + 1, '--format=zip')
except ValueError:
    # 無upload
    pass


def 讀(檔名):
    return open(os.path.join(os.path.dirname(__file__), 檔名)).read()


def 揣工具包(頭):
    'setup的find_packages無支援windows中文檔案'
    工具包 = []
    for 目錄, _, 檔案 in walk(頭):
        if '__init__.py' in 檔案:
            工具包.append(目錄.replace('/', '.'))
    return 工具包

setup(
    name='tai5-uan5_gian5-gi2_hok8-bu7',
    packages=揣工具包('臺灣言語服務'),
    version=版本,
    description='臺灣語言服務',
    long_description=讀('README.md'),
    author='薛丞宏',
    author_email='ihcaoe@gmail.com',
    url='https://xn--v0qr21b.xn--kpry57d/',
    download_url='https://github.com/sih4sing5hong5/tai5-uan5_gian5-gi2_hok8-bu7',
    keywords=[
        '語料庫', '語言合成', '機器翻譯',
        'Taiwan', 'Natural Language', 'Corpus',
        'Text to Speech', 'TTS',
        'Machine Translateion',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
    ],
    install_requires=[
        'tai5-uan5_gian5-gi2_tsu1-liau7-khoo3>=3.1.13',
        'pyro4',
        'gunicorn',
    ],
)
