from lxml import html
import requests
import urllib
import re
import logging

logging.basicConfig(level=logging.DEBUG)
s = requests.Session()
page = requests.get("http://narasimhadatta.info/bmtc_query.html")
tree = html.fromstring(page.content)

array_from = tree.xpath('//*[@name="from"]/option/text()')
array_to = tree.xpath('//*[@name="to"]/option/text()')

data= {
        'from' : 'Damodaranagar',
         'to' : 'Central Silk Board',
         'how' : 'Minimum Number of Hops',
        }
r = s.post('http://narasimhadatta.info/cgi-bin/find.cgi',data=data)
regex = re.escape('<tr><td>')+'(.+?)'+re.escape('</td><td>')+'(.+?)'+re.escape('</td><td>')+'(.+?)'+re.escape('</td><td>') + re.escape('<a href="/cgi-bin/find.cgi?route=')+'([0-9A-Z]{3,6})'
regex_a = re.escape('<a href="/cgi-bin/find.cgi?route=')+'([0-9A-Z]{3,6})'
pattern = re.compile(regex)
results = re.findall(pattern,r.text)
pattern_a = re.compile(regex_a)
results_a = re.findall(pattern_a,r.text)

#print results_a

#for j in range(0,len(results)):
 #   print results[j]


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
