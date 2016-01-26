'''
Created on Ja 2, 2016

@author: Alan Tai
'''
from google.appengine.ext import ndb

class WebLink(ndb.Model):
    link = ndb.StringProperty()
    title = ndb.StringProperty(required = False)
    
    create_datetime = ndb.DateTimeProperty(auto_now_add = True)
    update_datetime = ndb.DateTimeProperty(auto_now = True)
    
    
class WebLinkRoot(WebLink):
    pass

class WebLinkWine(WebLink):
    min_price = ndb.FloatProperty()
    avg_price = ndb.FloatProperty()
    max_price = ndb.FloatProperty()

class WebLinkWineTemp(WebLink):
    pass

class WinePriceInfo(ndb.Expando):
    pass