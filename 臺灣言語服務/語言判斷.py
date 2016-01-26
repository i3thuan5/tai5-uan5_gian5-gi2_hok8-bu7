import re


class 語言判斷:
    漢語語言 = re.compile('(臺語|台語|閩南|客家|客語|華語)')
    閩南語 = re.compile('(臺語|台語|閩南)')
    客話 = re.compile('(客家|客語|四縣|海陸|大埔|饒平|詔安)')

    @classmethod
    def 是漢語(cls, 語言):
        return cls.是閩南語(語言) or cls.是客話(語言) or \
            cls.漢語語言.match(語言) is not None

    @classmethod
    def 是閩南語(cls, 語言):
        return cls.閩南語.match(語言) is not None

    @classmethod
    def 是客話(cls, 語言):
        return cls.客話.match(語言) is not None
