from distutils.core import setup
import os
from 版本 import 版本

'''
tar無法度下傷長的檔案名，所以愛用zip
python setup.py sdist --format=zip upload
'''


def 讀(檔名):
    return open(os.path.join(os.path.dirname(__file__), 檔名)).read()

setup(
    name='tai5-uan5_gian5-gi2_hok8-bu7',
    packages=['臺灣言語服務'],
    version=版本,
    description='臺灣語言服務',
    long_description=讀('README.md'),
    author='薛丞宏',
    author_email='ihcaoe@gmail.com',
    url='http://意傳.台灣/',
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
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
    ],
    install_requires=[
        'tai5-uan5_gian5-gi2_tsu1-liau7-khoo3',
        'psycopg2',
        'django-cors-headers',
    ],
)
