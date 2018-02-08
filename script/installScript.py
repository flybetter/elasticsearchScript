#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@project= elasticsearchScript
@file= installScript
@author= wubingyu
@create_time= 2018/2/8 上午9:45
"""
import urllib2

url = "https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/zip/elasticsearch" \
      "/2.4.6/elasticsearch-2.4.6.zip"
print "downloading with elasticsearch 2.4.6"
f = urllib2.urlopen(url)
data = f.read()
with open("./elasticsearch-2.4.6.zip", "wb") as code:
    code.write(data)
