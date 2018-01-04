import codecs
import json
import os

import click

DICT_JSON = 'annotated_morph_dict_v2.json'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.environ['HOME']
if HOME_DIR:
    FOLDER = os.path.join(HOME_DIR, '.cdlimpatool')
else:
    FOLDER = os.path.join(ROOT_DIR, '.cdlimpatool')
JSON_PATH = os.path.join(FOLDER, DICT_JSON)


def load_annotations(infile, verbose=False):
    if verbose:
        click.echo('Loading annotations from {0}.'.format(infile))
    try:
        with codecs.open(infile, 'r', 'utf-8') as jsonfile:
            loaded_dict = json.load(jsonfile)
    except IOError:
        click.echo('First time usage : creating annotation json dictionary file as {0}.'.format(infile))
        if not os.path.exists(FOLDER):
            os.makedirs(FOLDER)
        store_annotations(infile, {}, verbose)
        with codecs.open(infile, 'r', 'utf-8') as jsonfile:
            loaded_dict = json.load(jsonfile)
    return loaded_dict


def store_annotations(outfile, loaded_dict, verbose=False):
    if verbose:
        click.echo('Storing annotations in {0}.'.format(outfile))
    with codecs.open(outfile, 'w', 'utf-8') as jsonfile:
        json.dump(loaded_dict, jsonfile, indent=2)


def line_process(line, loaded_dict):
    line = line.strip()
    if line[0] != '#':
        line_splitted = line.split('\t')
        if len(line_splitted) >= 2:
            form = line_splitted[1]
            if form not in loaded_dict:
                loaded_dict[form] = []
            if len(line_splitted) > 2:
                if len(line_splitted) > 4:
                    annotated_value = line_splitted[2:4]
                else:
                    annotated_value = line_splitted[2:]
                if annotated_value in list(map(lambda x: x['annotation'], loaded_dict[form])):
                    for i in range(len(loaded_dict[form])):
                        if loaded_dict[form][i]['annotation'] == annotated_value:
                            loaded_dict[form][i]['count'] += 1
                    loaded_dict[form] = sorted(loaded_dict[form], key=lambda k: k['count'], reverse=True)
                else:
                    annotation_dict = {'annotation': annotated_value, 'count': 1}
                    loaded_dict[form].append(annotation_dict)
            elif len(loaded_dict[form]) >= 1:
                line_next = []
                for i in range(len(loaded_dict[form])):
                    line_next.extend(loaded_dict[form][i]['annotation'])
                line_splitted += line_next
                line = '\t'.join(line_splitted)
    return line + '\n'


def file_process(infile, verbose=False, no_output=False):
    loaded_dict = load_annotations(JSON_PATH, verbose)
    outfolder = os.path.join(os.path.dirname(infile), 'output')
    if not no_output and not os.path.exists(outfolder):
        os.makedirs(outfolder)
    outfile_name = os.path.join(outfolder, os.path.basename(infile))
    if verbose and not no_output:
        click.echo('Writing in {0}.'.format(outfile_name))
    with codecs.open(infile, 'r', 'utf-8') as f:
        lines = f.readlines()
        if no_output:
            for line in lines:
                line_process(line, loaded_dict)
        else:
                with codecs.open(outfile_name, 'w+', 'utf-8') as f1:
                    for line in lines:
                        line = line_process(line, loaded_dict)
                        try:
                            f1.writelines(line)
                        except Exception:
                            click.echo('Could not write the following line. {0}.'.format(line))
    store_annotations(JSON_PATH, loaded_dict, verbose)



