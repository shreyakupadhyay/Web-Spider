#!/usr/bin/env python
'''
Author : Shreyak Upadhyay
Email : shreyakupadhyay07@gmail.com
Subject : running programs of various languages using one script .
Description: Using system calls and various python libraries compiling programs of various programming langauges using on single
script of python. 
'''

from lxml import html
import requests , urllib , re , logging


logging.basicConfig(level=logging.DEBUG)
s = requests.Session()
response = requests.get("http://narasimhadatta.info/bmtc_query.html")
tree = html.fromstring(response.content)

array_from = tree.xpath('//*[@name="from"]/option/text()')
array_to = tree.xpath('//*[@name="to"]/option/text()')

def getPath():
    data= {
            'from' : 'Damodaranagar',
             'to' : 'Central Silk Board',
             'how' : 'Minimum Number of Hops',
            }
    r = s.post('http://narasimhadatta.info/cgi-bin/find.cgi',data=data)
    regex = re.escape('<tr><td>')+'(.+?)'+re.escape('</td><td>')+'(.+?)'+re.escape('</td><td>')+'(.+?)'+re.escape('</td><td>') + re.escape('<a href="/cgi-bin/find.cgi?route=')+'([0-9A-Z]{3,6})'
    regex_a = re.escape('<a href="/cgi-bin/find.cgi?route=')+'([0-9A-Z]{3,6})'
    results = re.findall(re.compile(regex),r.text)
    results_a = re.findall(re.compile(regex_a),r.text)

getPath()


final = []
i=0
for j in range(0,len(results)):
    final.append([])
    final[j].append(results[j][0])
    final[j].append(results[j][1])
    final[j].append(results[j][2])
    final[j].append(results[j][3])
    i=i+1
    if(j<len(results)-1):
        while(str(results[j+1][3]) != str(results_a[i])):
            final[j].append(results_a[i])
            i=i+1
    else:
        while(i<len(results_a)):
            final[j].append(results_a[i])
            i=i+1

print final
