import sys
import unicodedata


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
    def __init__(self, inputFile):
        self.inputFileName = inputFile
        self.outputFilename = ""
        self.prefixMode = "o"
        self.tokens = []

    def convert(self):
        with open(self.inputFileName) as openedFile:
            for line in openedFile:
                self.__parse(line.strip())

    def writeToFile(self):
        outputFile = open(self.outputFilename + ".txt", "w")
        outputFile.writelines("#new_text=" + self.outputFilename + "\n")
        outputFile.writelines("# ID\tFORM\tSEGM\tXPOSTAG\tHEAD\tDEPREL\tMISC\n")
        for tok in self.tokens:
            outputFile.writelines(tok[0] + '\t' + tok[1] + '\n')
        outputFile.close()

    def __parse(self, line):
        tokenizedLine = line.split(" ")
        if line[0] == "&":
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


''' -------------------------- main -------------------------- '''

if __name__ == '__main__':
    try:
        pathToFile = sys.argv[1]
        convertor = ATFCONLConvertor(pathToFile)
        convertor.convert()
        convertor.writeToFile()
    except:
        print "Python Convertor Parsing Error!"
        sys.exit(1)

'''
Usage
$ python Convertor.py input.txt 
'''