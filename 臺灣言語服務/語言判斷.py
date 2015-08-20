import re


class 語言判斷:

    漢語語言 = re.compile('(臺語|台語|閩南|客家|客語|華語)')
    閩南語 = re.compile('(臺語|台語|閩南|)')
    客話 = re.compile('(客家|客語|四縣|海陸|大埔|饒平|詔安)')

    def 是漢語(self, 語言):
        return self.是閩南語(語言) or self.是客話(語言) or \
            self.漢語語言.match(語言) is not None

    def 是閩南語(self, 語言):
        return self.閩南語.match(語言) is not None

    def 是客話(self, 語言):
        return self.客話.match(語言) is not None
