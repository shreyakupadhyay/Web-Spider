import urllib
import requests
from bs4 import BeautifulSoup
import re
import MySQLdb
from threading import Thread


#lock = BoundedSemaphore(1)
"""Call this function once"""
brand = []
def brands():
    html = requests.get('http://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&filterNone=true')
    htmltext = html.text

    soup = BeautifulSoup(htmltext,'lxml')

    results = soup.findAll('li',attrs={'class':'facet'})
    for tag in results:
        #print tag['title']
        brand.append(tag['title'])
        if(tag['title']=='Zync'):
            break
    print brand
brands()
"""Store all brands in an array will save more 5-10s and not calling above function again and again"""
print len(brand)


def getproduct1(company):
        db = MySQLdb.connect('localhost','root',password,database)
        cursor = db.cursor()
        counter = 1
        name = 0
        while(name==0):
            try:
                url = 'http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?p%5B%5D=facets.brand%255B%255D%3D'+company+'&sid='+'tyy%2C4io'+ '&filterNone=true&start='+str(counter)+'&ajax=true'
            except Timeout:
                continue
            try:
                #html = requests.get(url,timeout=1)
                html = requests.get(url)
                print html
                htmltext = html.text
                regex_not_f = 'No matching products available.'
                if(regex_not_f in htmltext):
                    name = 1
                    break
                else:
                    soup = BeautifulSoup(htmltext,'lxml')
                    results = soup.findAll('div',attrs={'class':'pu-details lastUnit'})
                    j = 0
                    for div in results:
                        for data in div.findAll('a',attrs={'class':'fk-display-block'}):
                            value = data.get('title',data.get('href'))
                            if(value is None):
                                continue
                            else:
                                print data['href'] , 'number' , j
                                #print data['title']
                            j=j+1
                        dictionary = {'pu-old':'','pu-off-per else':'','fk-font-17 fk-bold 11':'','fk-font-17 fk-bold':'','pu-emi fk-font-12':''}
                        for data1 in div.findAll('span',attrs={'class':'pu-old'}):
                            if(data1.string!=None):
                                dictionary['pu-old'] = data1.strings
                            print data1.string
                        for data2 in div.findAll('span',attrs={'class':'pu-off-per else'}):
                            if(data2.string!=None):
                                dictionary['pu-off-per else'] = data2.string
                            print data2.string
                        for data3 in div.findAll('span',attrs={'class':'fk-font-17 fk-bold 11'}):
                            if(data3.string!=None):
                                dictionary['fk-font-17 fk-bold 11'] = data3.string
                            print data3.string
                        for data4 in div.findAll('span',attrs={'class':'fk-font-17 fk-bold'}):
                            if(data3.string!=None):
                                dictionary['fk-font-17 fk-bold'] = data4.string
                            print data4.string
                        for data5 in div.findAll('div',attrs={'class':'pu-emi fk-font-12'}):
                            if(data5.string!=None):
                                dictionary['pu-emi fk-font-12'] = data5.string
                            print data5.string
                        #for data5 in div.findAll('span',attrs={'class':'text'}):
                        #    print "YES6"
                        #    print data5.strin
                        #try:
                        #print dictionary['pu-old']
                        #cursor = connection.cursor()

                        cursor.execute("""INSERT INTO products VALUES (%s,%s,%s,%s,%s,%s)""",(data['href'],dictionary['pu-old'],dictionary['pu-off-per else'],dictionary['fk-font-17 fk-bold 11'],dictionary['fk-font-17 fk-bold'],dictionary['pu-emi fk-font-12']))

                        #except:
                        #    db.rollback()
                    counter = counter + j
                    print counter

            except requests.exceptions.ConnectionError:
                continue
        db.commit()
#all_sid_array = [['tyy%2C4io']]
#getproduct1(brand)
"""Multi Threading"""

threadlist = []
i=0
for j in range(0,6):
    for ele_arr in brand[1+i:51+i]:
        t = Thread(target=getproduct1,args=(ele_arr,))
        t.start()

        threadlist.append(t)
        i=i+50
#for ele_arr_th in threadlist:
#   ele_arr_th.join(
