'''
Subject : getting data of stocks .
Description:
Getting data of stocks by following a tutorial on youtube.. 
'''


from threading import Thread
import urllib, re ,MySQLdb

gmap ={}

def th(ur):
    url = "http://finance.yahoo.com/q?s="+ur
    response = urllib.urlopen(url).read()
    regex = '<span id="yfs_l84_' + ur.lower() + '">(.+?)</span>'
    pattern = re.compile(regex)
    results = re.findall(pattern,response)
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
    db = connect_database.cursor()  #this line is for selecting from the database;
    db.execute(query) #this line is used to execute a query
    row = db.fetchall()  #this line is to fetch data from the database
    connect_database.commit() 
