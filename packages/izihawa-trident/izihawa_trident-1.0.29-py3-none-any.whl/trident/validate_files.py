import glob
import os
import zipfile

from pypdf import PdfReader
from pypdf.errors import PdfReadError


def test_pdf(filepath):
    try:
        PdfReader(filepath)
    except PdfReadError:
        return False
    return True


def test_epub(filepath):
    the_zip_file = zipfile.ZipFile(filepath)
    ret = the_zip_file.testzip()
    if ret is not None:
        return False
    return True


def validate_files(path):
    for infile in glob.iglob(os.path.join(path, '*.*')):
        _, extension = infile.rsplit('.', 1)
        match extension:
            case 'pdf':
                if not test_pdf(infile):
                    print('broken', infile)
            case 'epub':
                if not test_epub(infile):
                    print('broken', infile)
            case _:
                print('unknown file')
