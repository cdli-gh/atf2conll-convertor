# ATF2CONLL Convertor

My Tool does one work, and one work well.

## Description

A CDLI-ATF to CDLI-Conll Python converter. The CDLI-ATF format is described [here](http://oracc.museum.upenn.edu/doc/help/editinginatf/cdliatf/index.html).

The full atf corpus is in [this repository](https://github.com/cdli-gh/data) [here](https://github.com/cdli-gh/data/blob/master/cdliatf_unblocked.atf.zip).

The goal is to take an atf file and convert it into one cdli-conll file per text.

Cdli-conll isn't an official format. It is our in-house conll version that we will then convert to conll-u format after the texts are annotated.

If you want to know more about conll-u, see [here](http://universaldependencies.org/format.html).

## Example

Here is an example of what the results should look like :
```csv
#new_text=P101049
# ID    FORM    SEGM    XPOSTAG HEAD    DEPREL  MISC
o.1.1   2(disz)
o.1.2   ma2
o.1.3   1(gesz2)
o.1.4   gur
o.1.5   2(ban2)-ta
o.1.6   ma2-lah5-bi
o.1.7   i3-ib2-u3
o.2.1   u4
o.2.2   3(u)
o.2.3   2(disz)-sze3
o.3.1   sze-bi
o.3.2   4(asz)
o.3.3   1(barig)
o.3.4   2(ban2)
o.3.5   gur
r.1.1   a-pi4-sal4{ki}-ta
r.2.1   nibru{ki}-sze3
r.2.2   siki
r.2.3   ba-a-si
r.3.1   giri3
r.3.2   ur-e11-e
r.4.1   mu
r.4.2   ur-bi2-lum{ki}
r.4.3   ba-hul
```

This is from the corresponding ATF :

```
&P101049 = AnOr 01, 058
#atf: lang sux
@tablet
@obverse
1. 2(disz) ma2 1(gesz2) gur 2(ban2)-ta ma2-lah5-bi i3-ib2-u3
#tr.en: 2 barges of 60 gur (capacity), 2 ban2 (per day) each, their skippers piloting,
2. u4 3(u) 2(disz)-sze3
#tr.en: for 32 days,
3. sze-bi 4(asz) 1(barig) 2(ban2) gur
#tr.en: its barley: 4 gur 1 barig 2 ban2;
# calculation: 32 × 2 × 0;0,2 = 4;1,2
@reverse
1. a-pi4-sal4{ki}-ta
#tr.en: from Apisal
2. nibru{ki}-sze3 siki ba-a-si
#tr.en: to Nippur, with wool filled,
3. giri3 ur-e11-e
#tr.en: via Ur-e’e,
4. mu ur-bi2-lum{ki} ba-hul
#tr.en: year: “Urbilum was destroyed.”
# Šulgi 45
```

You can see that the headers are not the same as in Conll-u.

The file should be names Pnnnnnn.conll , replace the Ns by the actual ID number of the text.
The ID is compose of 4 elements, : surface, column, line, word. the surface code is the abbreviation of the surface name (eg. obverse = o), if there are columns, there are none in this text, then add "col" and the column number, then line and word number.


# Installation

If you don't use `pip`, you're missing out.
Here are [installation instructions](https://pip.pypa.io/en/stable/installing/).

Simply run:

```bash
    $ git clone https://github.com/cdli-gh/atf2conll-convertor.git
    $ cd atf2conll-convertor
    $ pip install .
```

Or you can just do

    $ pip install git+git://github.com/cdli-gh/atf2conll-convertor.git

Or you can also do

    $ pip install git+https://github.com/cdli-gh/atf2conll-convertor.git

# Upgrading

If you already have installed it and want to upgrade the tool:

```bash
    $ cd atf2conll-convertor
    $ git pull origin master
    $ pip install . --upgrade
```

Or you can just do

    $ pip install git+git://github.com/cdli-gh/atf2conll-convertor.git --upgrade

Or you can also do

    $ pip install git+https://github.com/cdli-gh/atf2conll-convertor.git --upgrade


# Usage

To use it:

    $ atf2conll --help

*Only files with the .atf extension can be processed.  *
 
To run it on file:

    $ atf2conll -i ./resources/input.atf

To run it on folder:

    $ atf2conll -i ./resources

To see the console messages of the tool, use --verbose switch

    $ atf2conll -i ./resources  --verbose

If you don't give arguments, it will prompt for the path.  




