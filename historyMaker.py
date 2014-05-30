import time
from datetime import datetime
import urllib.request
import glob
import os


intervals=10*60 #10 minutes
def T():
    #returns a time string, usefull for the first row
    return time.strftime("%d/%m/%Y %H:%M:%S")

def isNYSEopen():
    #tells is NYSE is open right now
    #NYSE is closed in weekends and open between 14:30-21:00 UTC
    daysClosed = ['Saturday','Sunday']
    if time.strftime("%A") in daysClosed: return False #returns False if weekend
    From = 13.5
    To = 20
    now =(datetime.utcnow().hour)+(datetime.utcnow().minute/60)
    if From<now<To: return True
    else: return False

def price(Company):
    #returns the stock value
    query = Company
    req=urllib.request.Request('http://uk.finance.yahoo.com/q?s='+query+'&ql=1',headers = {'User-agent' : 'Opera/7.23 (Windows 98; U) [en]'})
    response = urllib.request.urlopen(req)
    html = response.read()
    html = html.decode('utf-8')
    try:
        Index_search='<span id="yfs_l84_'
        Index=html.index(Index_search)+len(Index_search)
        trimm=html[Index:]
        trimm=trimm[trimm.index('>')+1:]
        trimm=trimm[:trimm.index('<')]
        trimm=float(trimm.replace(',',''))
        return(trimm)
    except:
        return None

def searchResults(q):
    #returns the search results of a google query
    q=q.replace(' ','+')
    URL="https://www.google.co.uk/search?q="+q
    req=urllib.request.Request(URL,headers = {'User-agent' : 'Opera/7.23 (Windows 98; U) [en]'})
    response = urllib.request.urlopen(req)
    html = response.read()
    html = html.decode('utf-8')
    try:
        Index_search='>About '
        Index=html.index(Index_search)+len(Index_search)
        trimm=html[Index:]
        Index = trimm.index(' results ')
        trimm=trimm[:Index].replace(',','')
        trimm = int(trimm)
        return(trimm)
    except:
        return None

def tweetResults(q,minutes,attitude=None):
    #returns tweeter results per minute, add atribute ':)' or ':(' for good or bad reviews.
    #https://twitter.com/search?f=realtime&q=msft&src=typd
    url='https://twitter.com/search?f=realtime&q='+q+'&src=typd'
    if attitude == ':)':
        url='https://twitter.com/search?f=realtime&q='+q+'%20%3A%29&src=typd'
    if attitude == ':(':
        url='https://twitter.com/search?f=realtime&q='+q+'%20%3A(&&src=typd'
    req=urllib.request.Request(url,headers = {'User-agent' :'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'})
    response = urllib.request.urlopen(req)
    html = response.read()
    html = html.decode('utf-8')
    tweets = html.split('data-screen-name=')[1:-1]
    hour=datetime.utcnow().hour-7
    minute =datetime.utcnow().minute-minutes
    while minute <0:
        hour-=1
        minute+=60

    limit = hour+minute/60.0
    count = 0
    for tweet in tweets:
        time = tweet.split('&lt;span&gt;')[1].split(' ')[0].split(':')
        time = int(time[0])+int(time[1])/60.0
        if time>limit:
            count+=1
    return round(count /float(minutes),5)
def cycle():
    #iterates through the csv in data folder and updates them.


    #gets the header format and company symbols
    f=open('companies.txt','r')
    header = f.readline().replace('\n','').split('\t')
    companies=f.read().split('\n')
    f.close()
    spacer = 15
    toPrint=' '*spacer
    for i in header[1:]:
        toPrint=toPrint+i+' '*(spacer-len(i))

    print (toPrint)
    for company in companies:

        row=[]
        for column in header:
            if column == 'time': row.append(T())
            if column == 'price': row.append(str(price(company)))
            if 'search' in column:
                q=' '.join(column.split(' ')[1:])
                row.append(str(searchResults(company+" "+q)))
            if 'tweet' in column:
                q=' '.join(column.split(' ')[1:])
                row.append(str(tweetResults(company,intervals/60.0,q)))

        f = open('data/'+company+'.csv','a')
        f.write('\t'.join(row)+'\n')
        f.close()
        toPrint=company+' '*(spacer-len(company))

        for i in row[1:]:
            toPrint=toPrint+i+' '*(spacer-len(i))
        print(toPrint)

runAnyway=False
Break=False

while True:
    if isNYSEopen() or runAnyway:
        os.system('clear')
        print (T())
        cycle()
        if Break: break
        time.sleep(intervals)
    else:
        os.system('clear')
        print(T())
        print('NYSE is closed now.')
        time.sleep(intervals)
