from threading import Thread
import urllib
import re
import MySQLdb

gmap ={}

def th(ur):
    url_base = "http://finance.yahoo.com/q?s="+ur
    htmltext = urllib.urlopen(url_base).read()
    regex = '<span id="yfs_l84_' + ur.lower() + '">(.+?)</span>'
    pattern = re.compile(regex)
    results = re.findall(pattern,htmltext)
    gmap[ur] = results[0]
    try:
        print "the price of " + str(ur) + " is " + str(results)
    except:
        print "got an error"

symbollist = open("symbol.txt").read()
symbollist = symbollist.replace("\n",",").split(",")

threadlist = []


for sym in symbollist:
    t = Thread(target=th,args=(sym,))
    t.start()
    threadlist.append(t)

for sym_th in threadlist:
    sym_th.join() 


connect_database = MySQLdb.connect(host="127.0.0.1",user="root",passwd="*******",db="learning_for_scraping")

for key in gmap.keys():
    print key,gmap[key]
    query = "INSERT INTO about_stocks  (username,stocks_value) values (" 
    query = query + "'" + key + "'," + gmap[key] + ")"
    x = connect_database.cursor()  #this line is for selecting from the database;
    x.execute(query) #this line is used to execute a query
    row = x.fetchall()  #this line is to fetch data from the databse
    connect_database.commit() 
