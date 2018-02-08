#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= elasticsearchScript
@file= installScript2
@author= wubingyu
@create_time= 2018/2/8 上午9:57
"""
import urllib
import os
import tarfile
import zipfile
from subprocess import call
import shutil


def schedule(a, b, c):
    '''

    :param a: a count of blocks transferred
    :param b: a block size
    :param c: the total size of the file
    :return:
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print '%0.2f%%' % per


# def zipfile(filename):
#     azip = zipfile.ZipFile(filename)
#     return azip.filename

def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir): os.mkdir(unziptodir)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\', '/')

        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir): os.mkdir(ext_dir)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()


def addconfigurationvalue(filename):
    with open(filename + "/config/elasticsearch.yml", "a") as f:
        f.write("network.host: 0.0.0.0")


def start_elasticsearch(filename):
    os.system("echo \"hello world\"")
    os.system(fileName + "/bin/elasticsearch")


def copy_elasticsearch(filename, targetfilename):
    shutil.copytree(filename, targetfilename)
    return targetfilename


def install_plugins(filename):
    os.system(filename + "/bin/plugin install head")


def download_elasticsearch():
    url = "https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/zip/elasticsearch" \
          "/2.4.6/elasticsearch-2.4.6.zip"
    local = os.path.join('./', 'elasticsearch-2.4.6.zip')
    if not os.path.exists(fileZipName):
        print urllib.urlretrieve(url, local, schedule)


if __name__ == '__main__':

    fileZipName = "./elasticsearch-2.4.6.zip"
    fileName = "./elasticsearch-2.4.6"

    download_elasticsearch()

    if not os.path.exists(fileName):
        unzip_file(fileZipName, "./")

    addconfigurationvalue(fileName)
    start_elasticsearch(fileName)

    fileName2 = fileName + "-2"
    fileName3 = fileName + "-3"
    if not os.path.exists(fileName2):
        copy_elasticsearch(fileName, fileName2);
    if not os.path.exists(fileName3):
        copy_elasticsearch(fileName, fileName3);
