"""
Author : Shreyak Upadhyay
Email : shreyakupadhyay07@gmail.com
Subject : getting data from flipkart .
Description:
Getting data from flipkart on the basis of query search by the user.
"""
import urllib re , requests
from bs4 import BeautifulSoup
from threading import Thread


all_product = []

def getPage(query):
    url = "http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=search.flipkart.com&start=1&q="+product
    response = requests.get(url)
    return response.text
    


def getproduct1(product,page):
        url = "http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList?sid=search.flipkart.com&start="+page+"&q="+product
        response = requests.get(url)

        responsetext = response.text
        counter = 1
        try:
            regex_not_f = 'No matching products available.'
            if(regex_not_f in htmltext):
                print "There is no such product on flipkart"
            else:
                soup = BeautifulSoup(htmltext,'lxml')
                results = soup.findAll('div',attrs={'class':'pu-details lastUnit'})
                j = 0
                for div in results:
                    for data in div.findAll('a',attrs={'class':'fk-display-block'}):
                        value = data.get('title',data.get('href'))
                        if(value is None):
                            continue
                        j=j+1
                    dic_details = {"product name":"","old price":"","discount":"","actual price":"","price after discount":"","EMI":""}


                    data1 = div.findAll('span',attrs={'class':'pu-old'})
                    if(len(data1)!=0):
                        dic_details["old price"] = data1[0].string
                     #   print data1[0].string , "old price"
                    data2 = div.findAll('span',attrs={'class':'pu-off-per else'})
                    if(len(data2)!=0):
                        dic_details["discount"] = data2[0].string
                    #    print data2[0].string , "percent off"
                    data3 = div.findAll('span',attrs={'class':'fk-font-17 fk-bold 11'})
                    if(len(data3)!=0):
                        dic_details["actual price"] = data3[0].string
                   #     print data3[0].string , "actual price"
                    data4 = div.findAll('span',attrs={'class':'fk-font-17 fk-bold'})
                    if(len(data4)!=0):
                        dic_details["price after discount"] = data4[0].string
                  #      print data4[0].string , "price after discount"
                    data5 = div.findAll('div',attrs={'class':'pu-emi fk-font-12'})
                    if(len(data5)!=0):
                        dic_details["EMI"] = data5[0].string
                 #       print data5[0].string , "EMI"
                    data6 = div.findAll('a',{'class':'fk-display-block ssHashQuery'})
                    dic_details["product name"] = data6[0]["title"]
                #    print data6[0]["title"]  , "Product Name"
                    all_product.append(dic_details)
                counter = counter + j


        except requests.exceptions.ConnectionError:
            print "Problem in connection with the flipkart server"
#getproduct1()


"""
Multi Threading
"""
threadlist = []
i=1

for k in range(0,3):
    t = Thread(target=getproduct1,args=("iphone",str(i),))
    t.start()
    #t.join()
    threadlist.append(t)
    t.join()
    i = i+20
print all_product

# for i in range(0,3):
#     print t[i].join()

"""
returning a value from a function using threads.
"""
# from multiprocessing.pool import ThreadPool
# pool = ThreadPool(processes=3)

# async_result = pool.apply_async(getproduct1, ("iphone", str(i))) # tuple of args for foo

# # do some other stuff in the main process

# return_val = async_result.get()  # get the return value from your function.
# print return_val
