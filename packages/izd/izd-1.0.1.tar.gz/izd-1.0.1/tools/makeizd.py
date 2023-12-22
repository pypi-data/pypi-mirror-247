#!/usr/bin/env python3
"""
Make an .izd document from an HTML or Markdown file (plus images).

Uses pandoc to convert Markdown to HTML if the latter is not provided.

Author: Vlad Topan (vtopan/gmail)
"""
import argparse
import os
import subprocess
import tempfile

from libizd import IZDFile

parser = argparse.ArgumentParser(prog='makeizd', description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('izd_filename', help='output filename') 
parser.add_argument('filenames', help='the included filename(s): (at least) one HTML and / or Markdown document and images', nargs='+')
parser.add_argument('-t', '--title', help='document title (needed if not present in .md/.html')
args = parser.parse_args() 

# parse args
html = None
markdown = None
for e in args.filenames:
    ext = e.rsplit('.', 1)[-1].lower()
    if ext in ('md', 'markdown'):
        markdown = e
    elif ext in ('htm', 'html'):
        if e.lower().startswith('index.') or not html:
            html = e
if not (html or markdown):
    sys.exit('Need at least one HTML or Markdown document (preferrably both).')

# generate HTML if it doesn't exist
remove_html = False
if not html:
    tmp_file = tempfile.NamedTemporaryFile(suffix='index.html')
    tmp_file.close()
    html = tmp_file.name
    full_name = os.path.abspath(markdown)
    xargs = []
    if args.title:
        xargs += ['--metadata', f'title={args.title}']
    subprocess.check_call(['pandoc', '-f', 
            'markdown-markdown_in_html_blocks+implicit_header_references+superscript+subscript+simple_tables+table_captions+yaml_metadata_block+multiline_tables',
            '-t', 'html', '--mathjax', '-s', full_name, '-o', html] + xargs, cwd=os.path.dirname(tmp_file.name))
    args.filenames.append(html)
    remove_html = True

# create IZD
if not args.izd_filename.lower().endswith('.izd'):
    args.izd_filename += '.izd'
izd = IZDFile.new(args.izd_filename)
for e in args.filenames:
    if e == html:
        fn = 'index.html'
    elif e == markdown:
        fn = 'document.md'
    else:
        fn = e
    izd[fn] = open(e, 'rb').read()
izd.close()

# cleanup
if remove_html:
    os.remove(html)

print(f'Successfully created {args.izd_filename}.')
