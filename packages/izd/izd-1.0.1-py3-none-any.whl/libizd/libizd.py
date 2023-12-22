"""
Library which wraps ZIP processing and text / image retrieval and pandoc-based converters to
and from IZD (io-zipped-doc).

Author: Vlad Topan (vtopan/gmail)
"""
import os
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED

__VER__ = '1.0.1'

TEXT_FILE = 'document.md'
HTML_FILE = 'index.html'
IMAGE_FILE_PAT = 'image%03d.%s'


class IZDFile:

    def __init__(self, filename=None, create=False):
        self.filename = self.zf = None
        if filename:
            self.create(filename) if create else self.open(filename)


    @classmethod
    def new(cls, filename):
        return cls(filename, create=True)


    def create(self, filename):
        """
        Create a new IZF file.
        """
        self.filename = filename
        self.zf = ZipFile(filename, 'w', compression=ZIP_DEFLATED)


    def open(self, filename):
        """
        Open an IZF file.
        """
        self.filename = filename
        self.zf = ZipFile(filename)


    @property
    def text(self):
        """
        Read the (Markdown or HTML) text from the document.
        """
        filename = TEXT_FILE if TEXT_FILE in self else HTML_FILE
        return self.read_file(filename).decode()


    @text.setter
    def text(self, text):
        self.write_file(TEXT_FILE, text)


    @property
    def html(self):
        """
        Read the HTML text from the document.
        """
        return self.read_file(HTML_FILE).decode()


    @html.setter
    def html(self, html):
        self.write_file(HTML_FILE, html)


    @property
    def files(self):
        """
        List the files in the archive.
        """
        return self.zf.namelist()
        

    def read_file(self, filename):
        """
        Retrieve a file (e.g. image) from the document.
        """
        return self.zf.read(filename)


    def write_file(self, filename, contents):
        """
        Write a file (e.g. image) to the document.
        """
        compression = ZIP_STORED if filename.lower().endswith('.md') else ZIP_DEFLATED
        filename = os.path.basename(filename)
        self.zf.writestr(filename, contents, compress_type=compression)
    
    
    def __contains__(self, name):
        """
        Check if a filename exists in the archive.
        """
        return name in self.files


    def __getitem__(self, name):
        """
        Read a filename from the archive.
        """
        return self.read_file(name)
        

    def __setitem__(self, name, contents):
        """
        Write a file to the archive.
        """
        return self.write_file(name, contents)
        
    
    def close(self):
        """
        Close IZD object.
        """
        self.zf.close()
