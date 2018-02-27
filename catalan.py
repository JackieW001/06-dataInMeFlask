'''
Name: Catalan Historical Events Dataset
Our dataset contains the date and the event that occured on that date in the Catalan language. For example, the second entry of this dataset states that in the year -300, the first documented meteorological forecast was written by Teofrasto. 

Hyperlink: 
http://www.vizgr.org/historical-events/search.php?format=json&begin_date=-3000000&end_date=20151231&lang=ca

Import mechanism:
We made each event a separate collection in the Cieres database.
'''

from flask import Flask, render_template, request
import pymongo
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

teamname = 'wooJ-tabassumM'

connection = pymongo.MongoClient("homer.stuy.edu")
db = connection[teamname]
collection = db['catalan']

filename = "catalan.json"
f = open(filename,'r').read()

def join_duplicate_keys(ordered_pairs):
    d = {}
    for k, v in ordered_pairs:
        if k in d:
           if type(d[k]) == list:
               d[k].append(v)
           else:
               newlist = []
               newlist.append(d[k])
               newlist.append(v)
               d[k] = newlist
        else:
           d[k] = v
    return d

newdict = json.loads(f, object_pairs_hook=join_duplicate_keys)

el = newdict['result']

def updateDB(event_list):
    for x in el['event']:
        #print x
        date = x['date']
        #print date
        description = x['description']
        #print description
        lang = x['lang']
        #print lang
        granularity = x['granularity']
        #print granularity
        db.collection.insert({'date': date, "description": description, 'lang': lang, 'granularity': granularity})
        print "added successfully"

#print el
db.collection.drop()

#Adding to Database
#collection.insert_many(el)

#Searching by date
def date(d):
    c = db.collection.find({'date':d})
    for i in c:
        print i
date('-300')

#Searching by description
def desc(d):
    c = db.collection.find({'description':d})
    for i in c:
        print i
desc('Auge de Mero')

#Searching by date and description
def search (date, desc):
    c = db.collection.find({'date':date, 'description': desc})
    q = []
    for i in c:
        q.append(i)
    return q

app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])

def root():
    print request.args
    q =[]
    if request.args['Submitted'] == 'submit':
        print "SUBMITTED"
        date = request.args['date']
        desc = request.args['desc']
        #q = search(date,desc)
        q = [date,desc]
    #updateDB(el)
    return render_template("root.html", q=q)

if __name__ == '__main__':
    app.debug = True
    app.run()
