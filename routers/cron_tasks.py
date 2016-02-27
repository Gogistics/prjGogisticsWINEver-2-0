# -*- coding: utf-8 -*-
'''
Created on Dec 22, 2014
@author: Alan Tai
'''
from handlers.webapp2_auth import BaseHandler
from models.models_wine_info import WebLinkRoot, WebLinkWineTemp, WebLinkWine,\
    WinePriceInfo
from dictionaries.general import QueryInfo, Setting
from bs4 import BeautifulSoup
import webapp2, logging, re, urllib2, urlparse
from datetime import datetime

# set dict
dict_general = QueryInfo()

class TaskCrawlRootLinksDispatcher(BaseHandler):
    def get(self):
        self._read_feed()
    
    def _read_feed(self):
        """ crawling task """
        # temp root links
        root_list_temp = dict_general.wine_shops_urls
        
        # construct search list
        search_list = []
        query_root_entities = WebLinkRoot.query()
        if query_root_entities.count() > 0:
            for entity in query_root_entities:
                search_list.append({"title" : entity.title , "link" : entity.link})
        else:
            search_list = root_list_temp
            
        # start to crawl
        list_found_link = []
        while len(search_list) > 0:
            link = search_list.pop(0)["link"]
            parsed_str = urlparse.urlsplit(link)
            link_base = "{url_scheme}://{url_netloc}".format(url_scheme = parsed_str.scheme, url_netloc = parsed_str.netloc)
            
            
            try:
                req = urllib2.Request(link)
                response = urllib2.urlopen(req) # need to add new mechanism to prevent fetch javascript
                searched_page = response.read()
                soup = BeautifulSoup(searched_page)
                
                for found_link in soup.find_all('a'):
                    if found_link.get('href'):
                        match_group = re.match("http", found_link.get('href'), re.I)
                        full_href = ""
                        title = "NA"
                        
                        if not match_group:
                            full_href = "{href_link_base}{sub_href}".format(href_link_base = link_base, sub_href = found_link.get('href'))
                        else:
                            full_href = found_link.get('href')
                            
                        if found_link.contents and len(found_link.contents) > 0 and found_link.contents[0].string:
                            title = found_link.contents[0].string
                            
                        list_found_link.append({'title' : title, 'link' : full_href})
                        
            except urllib2.HTTPError, err:
                pass
                    
        
        # store result into db
        while len(list_found_link) > 0:
            new_link = list_found_link.pop(0)
            query = WebLinkWineTemp.query(WebLinkWineTemp.link == new_link['link'])
            if query.count() == 0:
                new_info = WebLinkWineTemp()
                new_info.link = new_link['link']
                new_info.title = new_link['title']
                new_info.put()
 

# crawl temp links
class TaskCrawlTempLinksDispatcher(BaseHandler):
    def get(self):
        # fetch entities from db
        entities = WebLinkWineTemp.query().fetch(15)
        search_list = []
        
        if entities:
            for entity in entities:
                search_list.append({'title' : entity.title, 'link' : entity.link})
                entity.key.delete()
        else:
            search_list = dict_general.wine_shops_urls
            
        # crawl website
        list_found_link = []
        while len(search_list) > 0:
            link = search_list.pop(0)['link']
            parsed_str = urlparse.urlsplit(link)
            link_base = "{url_scheme}://{url_netloc}".format(url_scheme = parsed_str.scheme, url_netloc = parsed_str.netloc)
            
            try:
                req = urllib2.Request(link)
                response = urllib2.urlopen(req) # need to add new mechanism to prevent fetch javascript
                searched_page = response.read()
                soup = BeautifulSoup(searched_page)
                
                for found_link in soup.find_all('a'):
                    if found_link.get('href'):
                        match_group = re.match("http", found_link.get('href'), re.I)
                        full_href = ""
                        title = "NA"
                        
                        if not match_group:
                            full_href = "{href_link_base}{sub_href}".format(href_link_base = link_base, sub_href = found_link.get('href'))
                        else:
                            full_href = found_link.get('href')
                            
                        if found_link.contents and len(found_link.contents) > 0 and found_link.contents[0].string:
                            title = found_link.contents[0].string
                            
                        list_found_link.append({'title' : title, 'link' : full_href})
            except urllib2.HTTPError, err:
                pass
                    
        # store result into db
        while len(list_found_link) > 0:
            new_link = list_found_link.pop(0)
            query = WebLinkWineTemp.query(WebLinkWineTemp.link == new_link['link'])
            if query.count() == 0:
                new_info = WebLinkWineTemp()
                new_info.link = new_link['link']
                new_info.title = new_link['title']
                new_info.put()
        
    

# categorize wine info
class TaskCategorizeWineInfoDispatcher(BaseHandler):
    def get(self):
        """ cron task """
        self._categorize()
        
    def _categorize(self):
        """ categorize wine info """
        entities = WebLinkWineTemp.query().fetch(50) # to avoid running datastore free quota limit
        for entity in entities:
            result = re.findall(r"BuyWine/Item/\d+|sku|skuIT-\d+|bwe\d+|wines/\d+|/wine/|Apply/Vintage/\d+", entity.link, re.I) # sku ; BuyWine/Item ; bwe
            query = WebLinkWine.query(WebLinkWine.link == entity.link)
            if result and query.count() == 0:
                new_wine_info = WebLinkWine()
                new_wine_info.link = entity.link
                new_wine_info.title = entity.title
                new_wine_info.put()

# find price
class TaskSearchPriceDispatcher(BaseHandler):
    def get(self):
        self._search_price()
    
    def _search_price(self):
        entities = WebLinkWine.query().fetch(50)
        
        for entity in entities:
            # belmontwine
            match_result = re.findall(r'^(?=http://www.belmontwine.com/)(?=bwe/\d+)$', entity.link, re.I)
            if match_result:
                req = urllib2.Request(entity.link)
                response = urllib2.urlopen(req) # need to add new mechanism to prevent fetch javascript
                searched_page = response.read()
                soup = BeautifulSoup(searched_page)
                
                found_price = soup.find('td', { "class" : "detail-price-txt" })
                price = found_price.string.strip()
                if price != '':
                    wine_price = WinePriceInfo(link = entity.link,
                                               current_price = price,
                                               created_datetime = datetime.now())
                    wine_price.put()
                    
            # winebid
            match_result = re.findall(r'^(?=http://www.winebid.com/Apply/Vintage/)(?=\d+).*$', entity.link, re.I)
            if match_result:
                req = urllib2.Request(entity.link)
                response = urllib2.urlopen(req) # need to add new mechanism to prevent fetch javascript
                searched_page = response.read()
                soup = BeautifulSoup(searched_page)
                
                found_price = soup.find('div', { "class" : "price" } )
                price = found_price.string.strip()
                if price != '':
                    wine_price = WinePriceInfo(link = entity.link,
                                               current_price = price,
                                               created_datetime = datetime.now())
                    wine_price.put()
                        
            # k&l
            match_result = re.findall(r'^(?=http://www.klwines.com/)(?=.*sku=\d+)$', entity.link, re.I)
            if match_result:
                req = urllib2.Request(entity.link)
                response = urllib2.urlopen(req) # need to add new mechanism to prevent fetch javascript
                searched_page = response.read()
                soup = BeautifulSoup(searched_page)
                
                found_price = soup.find('span', { "class" : "price" })
                price_elem = found_price.find('strong')
                price = price_elem.string.strip()
                if price != '':
                    wine_price = WinePriceInfo(link = entity.link,
                                               current_price = price,
                                               created_datetime = datetime.now())
                    wine_price.put()

# configuration
dict_setting = Setting()
config = dict_setting.config_setting

# app
app = webapp2.WSGIApplication([
    webapp2.Route(r'/cron_tasks/crawl_root_links', TaskCrawlRootLinksDispatcher, name = 'crawl_root_links'),
    webapp2.Route(r'/cron_tasks/crawl_temp_links', TaskCrawlTempLinksDispatcher, name = 'crawl_temp_links'),
    webapp2.Route(r'/cron_tasks/categorize_wine_info', TaskCategorizeWineInfoDispatcher, name = "categorize_wine_info"),
    webapp2.Route(r'/cron_tasks/search_wine_price', TaskSearchPriceDispatcher, name = "search_wine_price")
], debug=True, config=config)

# log
logging.getLogger().setLevel(logging.DEBUG)