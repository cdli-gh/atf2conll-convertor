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

ATF_FRAGMENT_SINGLE = """\
&P222243 = Test Fragment
#atf: lang sux
@tablet
@fragment a
1. sze-bi gur
2. mu ba-hul
"""

ATF_FRAGMENT_MULTI = """\
&P222243 = Test Multi Fragment
#atf: lang sux
@tablet
@fragment a
1. sze-bi gur
@fragment b
1. mu ba-hul
"""

ATF_FRAGMENT_NO_LETTER = """\
&P222243 = Test No Letter Fragment
#atf: lang sux
@tablet
@fragment
1. sze-bi gur
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


def test_fragment_ids_have_surface_prefix():
    """@fragment surface should produce IDs starting with 'f', not a bare dot."""
    fname, c = make_convertor(ATF_FRAGMENT_SINGLE)
    try:
        c.convert()
        for token_id, _ in c.tokens:
            assert not token_id.startswith('.'), (
                f"ID '{token_id}' starts with dot — fragment surface prefix missing"
            )
        assert c.tokens[0][0] == 'f.a.1.1'
        assert c.tokens[1][0] == 'f.a.1.2'
        assert c.tokens[2][0] == 'f.a.2.1'
        assert c.tokens[3][0] == 'f.a.2.2'
    finally:
        os.unlink(fname)


def test_fragment_ids_are_unique_across_fragments():
    """Multiple @fragment sections must produce globally unique IDs."""
    fname, c = make_convertor(ATF_FRAGMENT_MULTI)
    try:
        c.convert()
        id_list = [tok[0] for tok in c.tokens]
        assert len(id_list) == len(set(id_list)), "Duplicate IDs found in multi-fragment text"
        assert c.tokens[0][0] == 'f.a.1.1'
        assert c.tokens[2][0] == 'f.b.1.1'
    finally:
        os.unlink(fname)


def test_fragment_no_letter_has_surface_prefix():
    """@fragment with no letter should still produce IDs starting with 'f'."""
    fname, c = make_convertor(ATF_FRAGMENT_NO_LETTER)
    try:
        c.convert()
        for token_id, _ in c.tokens:
            assert not token_id.startswith('.'), (
                f"ID '{token_id}' starts with dot — fragment surface prefix missing"
            )
        assert c.tokens[0][0].startswith('f.')
    finally:
        os.unlink(fname)
