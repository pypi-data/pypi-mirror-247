# This file is placed in the Public Domain.
#
#


"wrap on lines with x length"


import textwrap


def __dir__():
    return (
         'Textwrap',
    )


class TextWrap(textwrap.TextWrapper):

    def __init__(self):
        super().__init__()
        self.break_long_words = False
        self.drop_whitespace = False
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 400
