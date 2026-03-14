import os
import tempfile
import pytest
from atf2conll_convertor.convertor import ATFCONLConvertor


ATF_SIMPLE = """\
&P101049 = AnOr 01, 058
#atf: lang sux
@tablet
@obverse
1. 2(disz) ma2 gur
@reverse
1. a-pi4-sal4{ki}-ta
"""

ATF_BILINGUAL = """\
&P222243 = Test Bilingual
#atf: lang akk
@tablet
@obverse
1. a-na _lu2 dumu_-szu2 iqbi
2. _sze gur_ ba-an-si
"""


def make_convertor(atf_content):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.atf', delete=False, encoding='utf-8') as f:
        f.write(atf_content)
        fname = f.name
    outfolder = os.path.join(os.path.dirname(fname), 'output')
    os.makedirs(outfolder, exist_ok=True)
    return fname, ATFCONLConvertor(fname, verbose=False)


def test_basic_conversion():
    fname, c = make_convertor(ATF_SIMPLE)
    try:
        c.convert()
        assert c.tokens == [
            ('o.1.1', '2(disz)'),
            ('o.1.2', 'ma2'),
            ('o.1.3', 'gur'),
            ('r.1.1', 'a-pi4-sal4{ki}-ta'),
        ]
    finally:
        os.unlink(fname)


def test_underscore_removal():
    fname, c = make_convertor(ATF_BILINGUAL)
    try:
        c.convert()
        forms = [form for _, form in c.tokens]
        for form in forms:
            assert '_' not in form, f'Underscore found in output token: {form!r}'
        assert forms == ['a-na', 'lu2', 'dumu-szu2', 'iqbi', 'sze', 'gur', 'ba-an-si']
    finally:
        os.unlink(fname)


def test_special_chars_removed():
    atf = """\
&P000001 = Test
#atf: lang sux
@tablet
@obverse
1. sze# [ba]-hul <du> mu!
"""
    fname, c = make_convertor(atf)
    try:
        c.convert()
        forms = [form for _, form in c.tokens]
        for form in forms:
            for ch in ('#', '[', ']', '<', '>', '!', '?'):
                assert ch not in form, f'{ch!r} found in output token: {form!r}'
    finally:
        os.unlink(fname)
