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
import stat
import multiprocessing
from ftplib import FTP
import paramiko
import time


# import pexpect


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


def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        # print arcname
        zf.write(tar, arcname)
    zf.close()
    return zipfilename


def addconfigurationvalue(filename):
    result = add_cluster_ip()
    with open(filename + "/config/elasticsearch.yml", "a") as f:
        f.write("network.host: 0.0.0.0")
        f.write("\n")
        f.write(result)
        f.write("node.max_local_storage_nodes: 1 ")


def start_elasticsearch(filename):
    os.system(fileName + "/bin/elasticsearch -Des.insecure.allow.root=true")


def copy_elasticsearch(filename, targetfilename):
    if not os.path.exists(targetfilename):
        shutil.copytree(filename, targetfilename)

    return targetfilename


def install_plugins(filename):
    os.system(filename + "/bin/plugin install mobz/elasticsearch-head")


def download_elasticsearch():
    url = "https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/zip/elasticsearch" \
          "/2.4.6/elasticsearch-2.4.6.zip"
    local = os.path.join('./', 'elasticsearch-2.4.6.zip')
    if not os.path.exists(fileZipName):
        print urllib.urlretrieve(url, local, schedule)


def add_authority(filename):
    os.chmod(filename + "/bin/elasticsearch", stat.S_IRWXU)
    os.chmod(filename + "/bin/plugin", stat.S_IRWXU)


class MultiProcess(multiprocessing.Process):
    def __init__(self, filename, ipaddress, password):
        multiprocessing.Process.__init__(self)
        self.filename = filename
        self.ipaddress = ipaddress
        self.password = password

    def run(self):
        print 'filename:' + self.filename
        print 'ipaddress:' + self.ipaddress
        print 'password:' + self.password
        transfer(self.filename, self.ipaddress, self.password)


def read_ipaddress(serverconfig):
    with open(serverconfig, "r") as f:
        return f.readlines()


def transfer(filename, ipaddress, password):
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ipaddress.replace("#", ""), 22, "root", password)
    except:
        print "can't connect to the server,please check your server or password"

    stdin, stdout, stdeer = ssh.exec_command("ls " + dirname)

    print stdout.readline()

    if stdout.readline() == '':
        ssh.exec_command(" mkdir " + dirname)

    not_exist = check_elasticsearch_process(ssh)

    print "whether or not elasticsearch services is running:" + str(not_exist)

    if not_exist and not ipaddress.startswith('#'):
        start_remote_elasticsearch(ssh, filename, ipaddress)
    else:

        if ipaddress.startswith("#"):
            kill_elasticsearch(ssh, ipaddress)
        else:
            print "server ip:" + ipaddress + " already run elasticsearch"

    clean(filename)

    ssh.close()


def kill_elasticsearch(ssh, ipaddress, ):
    ssh.exec_command("kill -9 $(ps -ef|grep elasticsearch |grep -v grep|awk '{print $2}')")
    print "server ip:" + ipaddress + " close the elasticsearch"


def clean(filename):
    if os.path.exists("./" + filename.split("/")[1] + ".zip"):
        os.remove("./" + filename.split("/")[1] + ".zip")
    shutil.rmtree("./" + filename)


def check_elasticsearch_process(ssh):
    stdin, stdout, stdeer = ssh.exec_command("ps -ef|grep elasticsearch|grep -v grep")
    return len(stdout.read()) == 0


def start_remote_elasticsearch(ssh, filename, ipaddress):
    sftp = ssh.open_sftp()

    stdin, stdout, stdeer = ssh.exec_command("ls " + dirname)

    print stdout.readline()

    if stdout.readline() == '':
        filenamezip = zip_dir(filename, filename.split("/")[1] + ".zip")

        print "filenamezip :" + filenamezip

        sftp.put(filenamezip, filenamezip)

        ssh.exec_command("nohup unzip " + filenamezip + " -d " + dirname)

        time.sleep(10)

        ssh.exec_command("chmod 777 ./" + dirname + "/bin/elasticsearch")

    ssh.exec_command("nohup ./" + dirname + "/bin/elasticsearch -Des.insecure.allow.root=true")

    print "server ip:" + ipaddress + " installed elasticsearch successful"


def transfer_ftp(filename, ipaddress, password, username="root"):
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(ipaddress, username, password)
    ftp.login(username, password)


def start_multielasticsearch(filename, ipaddress, password, username):
    # ssh = paramiko.SSHClient()
    # ssh.connect(ipaddress, 22, username, password)
    # ssh.set_log_channel(2)
    # stdin, stdout, stdeer = ssh.exec_command("unzip " + filename)
    # print stdout
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ipaddress, 22, "root", password)
    stdin, stdout, stdeer = ssh.exec_command("ls")
    print stdout.readlines()


def add_cluster_ip():
    result = r'discovery.zen.ping.unicast.hosts: ["127.0.0.1"'
    with open("../config.txt") as f:
        for line in f:
            result += r',"' + line.strip().split(" ")[0] + '"'
    result += ']'
    print "ipaddress :" + result
    return result


if __name__ == '__main__':

    global dirname

    dirname = "elasticsearch_dir"

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    os.chdir(dirname)

    fileZipName = "./elasticsearch-2.4.6.zip"
    fileName = "./elasticsearch-2.4.6"
    serverConfig = "../config.txt"

    download_elasticsearch()

    if not os.path.exists(fileName):
        unzip_file(fileZipName, "./")
        addconfigurationvalue(fileName)
        add_authority(fileName)
        install_plugins(fileName)

    if not os.path.exists(serverConfig):
        fileName2 = fileName + "-2"
        fileName3 = fileName + "-3"
        if not os.path.exists(fileName2):
            copy_elasticsearch(fileName, fileName2);
        if not os.path.exists(fileName3):
            copy_elasticsearch(fileName, fileName3);

        p1 = multiprocessing.Process(target=start_elasticsearch, args=(fileName,))
        p1.start()
        p2 = multiprocessing.Process(target=start_elasticsearch, args=(fileName2,))
        p3 = multiprocessing.Process(target=start_elasticsearch, args=(fileName3,))

        p2.start()
        p3.start()

    else:
        # p1 = multiprocessing.Process(target=start_elasticsearch, args=(fileName,))
        # p1.start()
        line_data = read_ipaddress(serverConfig)
        for i, line in enumerate(line_data):
            copy_file_name = copy_elasticsearch(fileName, fileName + '-' + str(i))
            p = MultiProcess(copy_file_name, line.split(" ")[0].strip(), line.split(" ")[1].strip())
            p.start()
