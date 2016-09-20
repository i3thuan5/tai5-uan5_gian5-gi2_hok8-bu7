import re


class 漢語語音處理:
    _切漢語韻 = re.compile('.ⁿ|m̩|ŋ̩|[^ⁿ]')

    @classmethod
    def 切漢語韻(cls, 韻):
        return cls._切漢語韻.findall(韻)
