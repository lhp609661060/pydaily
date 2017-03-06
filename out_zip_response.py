# coding=utf8

"""
django 输出zip文件
"""

import tempfile
import zipfile
import requests


from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse

def out_zip_response(zip_file, zip_name):

    wrapper = FileWrapper(zip_file)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename={}.zip'.format(zip_name)
    response['Content-Length'] = zip_file.tell()

    return response

def out_zip_response_by_file_name(filenames, zip_name):

    temp_zip = tempfile.TemporaryFile()

    for filename in filenames:

        archive = zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED)
        archive.write(filename, filename)
        archive.close()

    temp_zip.seek(0)

    return out_zip_response(temp_zip, zip_name)

def out_zip_response_by_urls(urls, zip_name):

    temp_zip = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED)

    for url in urls:
        _tempf = tempfile.NamedTemporaryFile()
        _f = requests.get(url, stream=True)

        for chun in _f.iter_content(1024):
            if chun:
                _tempf.write(chun)

        _tempf.seek(0)
        archive.write(_tempf.name, url.split('/')[-1])

    archive.close()
    temp_zip.seek(0)
    
    return out_zip_response(temp_zip, zip_name)