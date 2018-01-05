import os
import click
from stat import ST_MODE, S_ISREG

from atf2conll_convertor.convertor import ATFCONLConvertor


def file_process(infile, verbose=False):
    outfolder = os.path.join(os.path.dirname(infile), 'output')
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    convertor = ATFCONLConvertor(infile, verbose)
    convertor.convert()
    convertor.write2file()


def check_and_process(pathname, verbose=False):
    mode = os.stat(pathname)[ST_MODE]
    if S_ISREG(mode) and pathname.lower().endswith('.atf'):
        # It's a file, call the callback function
        if verbose:
            click.echo('Processing {0}.'.format(pathname))
        file_process(pathname, verbose)


@click.command()
@click.option('--input_path', '-i', type=click.Path(exists=True, writable=True), prompt=True, required=True,
              help='Input the file/folder name.')
@click.option('-v', '--verbose', default=False, required=False, is_flag=True, help='Enables verbose mode')
@click.version_option()
def main(input_path, verbose):
    """My Tool does one work, and one work well."""
    if os.path.isdir(input_path):
        with click.progressbar(os.listdir(input_path), label='Converting the files') as bar:
            for f in bar:
                pathname = os.path.join(input_path, f)
                check_and_process(pathname, verbose)
    else:
        check_and_process(input_path, verbose)
