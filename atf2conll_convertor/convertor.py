import unicodedata
import codecs
import click
import os

OUTPUT_FOLDER = 'output'


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


class ATFCONLConvertor:
    def __init__(self, inputFile, verbose):
        self.inputFileName = inputFile
        self.outfolder = os.path.join(os.path.dirname(self.inputFileName), OUTPUT_FOLDER)
        self.verbose = verbose
        self.outputFilename = ""
        self.prefixMode = "o"
        self.tokens = []

    def convert(self):
        if self.verbose:
            click.echo('Reading file {0}.'.format(self.inputFileName))
        with codecs.open(self.inputFileName, 'r', 'utf-8') as openedFile:
            for line in openedFile:
                self.__parse(line.strip())

    def write2file(self):
        outfile_name = os.path.join(self.outfolder, self.outputFilename+".conll")
        with codecs.open(outfile_name, 'w+', 'utf-8') as outputFile:
            outputFile.writelines("#new_text=" + self.outputFilename + "\n")
            outputFile.writelines("# ID\tFORM\tSEGM\tXPOSTAG\tHEAD\tDEPREL\tMISC\n")
            for tok in self.tokens:
                outputFile.writelines(tok[0] + '\t' + tok[1] + '\n')

    def __parse(self, line):
        tokenizedLine = line.split(" ")
        if len(line) == 0:
            pass
        elif line[0] == "&":
            if len(self.tokens) > 0:
                self.write2file()
                self.tokens = []
            firstword = tokenizedLine[0].lstrip("&")
            self.outputFilename = firstword
        elif line[0] == "@":
            firstword = tokenizedLine[0].lstrip("@")
            if firstword == "obverse":
                self.prefixMode = "o"
            elif firstword == "reverse":
                self.prefixMode = "r"
        elif line[0] != "#" and is_number(line[0]):
            linenumber = tokenizedLine[0].rstrip(".")
            tokensToProcess = tokenizedLine[1:]
            for i in range(len(tokensToProcess)):
                IDlist = [self.prefixMode, linenumber, str(i + 1)]
                ID = ".".join(IDlist)
                self.tokens.append((ID, tokensToProcess[i]))

