# coding=utf8

"""
阿里云人脸识别测试代码
"""

import urllib
import urllib2
import sys
import ssl
import requests as R
import base64
import json
import argparse


host = 'https://dm-23.data.aliyun.com'
path = '/rest/160601/face/age_detection.json'
method = 'POST'
appcode = '189a2c82bbc44729964d98bcdc5ed1ef'
querys = ''
bodys = {}
url = host + path

def face_age_by_url(iamge_url):
	base64_string = base64.b64encode(R.get(iamge_url).content)
	return face_age(base64_string)

def face_age_by_iamge(image_path):
	base64_string = base64.b64encode(open(image_path, 'rb').read())
	return face_age(base64_string)

def face_age(base64_string):
	bodys[''] = "{\"inputs\":[{\"image\":{\"dataType\":50,\"dataValue\":\""+base64_string+"\"}}]}"
	post_data = bodys['']
	request = urllib2.Request(url, post_data)
	request.add_header('Authorization', 'APPCODE ' + appcode)
	request.add_header('Content-Type', 'application/json; charset=UTF-8')
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	response = urllib2.urlopen(request, context=ctx)
	content = response.read()
	data = json.loads(content)
	value = json.loads(data['outputs'][0]['outputValue']['dataValue'])
	return value['age'][0]


parser = argparse.ArgumentParser()
parser.add_argument("t", help="type url,path")
parser.add_argument("v", help="value")
args = parser.parse_args()

if args.t == 'url':
	print face_age_by_url(args.v)

if args.t == 'path':
	print face_age_by_iamge(args.v)


# img = 'https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1489114799&di=b03226309509ee030a0beccde14aad2f&src=http://pic16.nipic.com/20110905/3576333_090635527162_2.jpg'

# base64_string = base64.b64encode(R.get(img).content)

# # base64_string = base64.b64encode(open('/Users/lhp/Downloads/aaa.jpg', 'rb').read())

# bodys[''] = "{\"inputs\":[{\"image\":{\"dataType\":50,\"dataValue\":\""+base64_string+"\"}}]}"
# post_data = bodys['']
# request = urllib2.Request(url, post_data)
# request.add_header('Authorization', 'APPCODE ' + appcode)
# request.add_header('Content-Type', 'application/json; charset=UTF-8')
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
# response = urllib2.urlopen(request, context=ctx)
# content = response.read()
# if (content):
#     print(content)
#     print json.loads(content)