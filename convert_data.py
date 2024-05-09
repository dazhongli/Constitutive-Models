import argparse
import re

def main(args):
    with open(args.input_file, 'r') as fin:
        data = fin.read()
    data_modified = data.replace(r'$$', ' ')
    pattern = r'\[label@(.*)\]'
    replacement = r'{\\label{\1}}'
    data_modified = re.sub(pattern, replacement, data_modified)
    with open(args.output_file, 'w') as fout:
        fout.write(data_modified)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a Markdown file and output a modified version.')
    parser.add_argument('input_file', help='the input Markdown file')
    parser.add_argument('output_file', help='the output file for the modified content')
    args = parser.parse_args()
    main(args)
