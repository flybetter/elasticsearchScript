#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= elasticsearchScript
@file= installScript3
@author= wubingyu
@create_time= 2018/2/9 下午2:52
"""

import paramiko
from ftplib import FTP


def transfer(filename, ipaddress, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ipaddress, 22, "root", password)

    # stdin, stdout, stdeer = ssh.("cd /opt")
    # print stdout.readlines()

    stdin, stdout, stdeer = ssh.exec_command("pwd")
    print stdout.read()
    #
    # sftp = ssh.open_sftp()
    # sftp.put("elasticsearch-2.4.6-0.zip", "elasticsearch-2.4.6-0.zip")

    stdin, stdout, stdeer = ssh.exec_command("nohup ./bin/elasticsearch")
    print stdout


def transfer_ftp(filename, ipaddress, password, username="root"):
    ftp = FTP(ipaddress)
    ftp.set_debuglevel(2)
    ftp.login(username, password)
    ftp.cwd("/root")
    ftp.retrlines("LIST")
    ftp.retrbinary('RETR README', open('README', 'wb').write)
    ftp.quit()


def test_ps(ipaddress, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(ipaddress, 22, "root", password)
    stdin, stdout, stdeer = ssh.exec_command("ps -ef|grep elasticsearch|grep -v grep")
    print len(stdout.read())

    return len(stdout.read()) == 0


def test_config():
    result = r'discovery.zen.ping.unicast.hosts: ["127.0.0.1"'
    with open("config.txt") as f:
        for line in f:
            result += r',"' + line.strip().split(" ")[0] + '"'

    result += ']'

    print "result:" + result


if __name__ == '__main__':
    # transfer("11", "192.168.105.234", "doucare")

    # transfer_ftp("1", "192.168.105.234", "doucare")

    # aa =test_ps("192.168.105.234", "doucare")
    # print not aa
    test_config()
