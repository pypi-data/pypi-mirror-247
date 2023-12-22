# izd

The IZD (io-zipped-doc) file format, which is essentially a ZIP archive with an `index.html` file
containing the actual document, optionally the Markdown text as `document.md` and `image<num>.<ext>`
files containing the images.

## vizd/vizd.pyw

This is a Python / Qt WebView-based viewer for IZD files. TODO: pack it as an .exe.

## libizd

The library which wraps ZIP processing and text / image retrieval and pandoc-based converters to
and from IZD.

## tools/makeizd.py

Command-line creation tool for IZD documents. Takes an HTML and / or a Markdown file + images as
input. Generates the HTML from Markdown if needed using pandoc.

## See also

- <https://gitlab.com/vtopan/io-scripts/-/blob/master/getdoc.py> can download an article from the
   Internet and save it as an .IZD file
