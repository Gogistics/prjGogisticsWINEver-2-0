# -*- coding: utf-8 -*-
'''
Created on Dec 24, 2014
@author: Alan Tai
'''
from handlers.webapp2_auth import BaseHandler
from dictionaries.general import QueryInfo, Setting
from bs4 import BeautifulSoup
import jinja2, webapp2, logging, json, re, urllib2

# jinja environment
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('static/templates'))

# dict
dict_query_info = QueryInfo()

class GetQueryKeywordsHandler(BaseHandler):
    def post(self):
        """ query mechanism for wine searcher """
        query_results = {u'status': True}
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(query_results, ensure_ascii = False).encode('utf8'))
        
class GetTopFavoritesHandler(BaseHandler):
    def post(self):
        """ query mechanism for wine searcher """
        query_results = []
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(query_results, ensure_ascii = False).encode('utf8'))
    
# configuration
dict_setting = Setting()
config = dict_setting.config_setting

# app
app = webapp2.WSGIApplication([
    webapp2.Route(r'/wine_info/get_query_keywords', GetQueryKeywordsHandler, name='get_query_keywords'),
    webapp2.Route(r'/wine_info/get_top_favorites', GetTopFavoritesHandler, name='get_top_favorites')
], debug=True, config=config)

# log
logging.getLogger().setLevel(logging.DEBUG)