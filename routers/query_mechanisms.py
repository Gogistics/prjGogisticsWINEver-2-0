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

class WineQueryHandler(BaseHandler):
    def post(self):
        """ query mechanism for wine searcher """
        query_wine_info = self.request.get('query_info')
        query_wine_info = re.sub(r'\s|-','+',query_wine_info)
        
        # build query string for snooth
        user_ip = self.request.remote_addr if (self.request.remote_addr) else dict_query_info.snooth_api['default_ip']
            
        query_str = u'{base_url}&ip={user_ip}&q={query_wine_info}&s={order_by}'.format(base_url = dict_query_info.snooth_api['base_url'],
                                                                                        user_ip = user_ip,
                                                                                        query_wine_info = urllib2.quote(query_wine_info.encode('utf-8')),
                                                                                        order_by = 'price+asc' )
        snooth_query_result = json.loads(self._get_query_result_from_snooth(query_str))
        
        # build query string for wine searcher
        query_str_for_wine_searcher = u'{reroute_url}?query_str={query_str}'.format( reroute_url = dict_query_info.wine_searcher_api['reroute_url'], query_str = query_wine_info )
        wine_searcher_query_result = self._get_query_result_from_wine_searcher(query_str_for_wine_searcher)
        
        # vivino
        query_str_for_vivino = u'{search_url}{query_str}'.format(search_url = dict_query_info.vivino_api['search_url'], query_str = query_wine_info)
        vivino_query_result = self._get_query_result_from_vivino(query_str_for_vivino)
        
        # build response json
        query_results = { 'snooth_query_result' : snooth_query_result,
                          'wine_searcher_query_result' : wine_searcher_query_result,
                          'vivino_query_result': vivino_query_result}
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(query_results, ensure_ascii = False).encode('utf8'))
        
    def _get_query_result_from_snooth(self, arg_query_str):
        """ get query result from Snooth """
        req = urllib2.Request(arg_query_str)
        return urllib2.urlopen(req).read()
        
    def _get_query_result_from_wine_searcher(self, arg_query_str):
        """ get query result from wine searcher """
        req = urllib2.Request(arg_query_str, headers = dict_query_info.wine_searcher_api['headers']) 
        response = urllib2.urlopen(req)
        soup = BeautifulSoup(response)
        table = soup.find('table', {'id': 'wine_list'})
        trs = table.find_all('tr')
        result_list = []
        for count, tr in enumerate(trs):
            wine_name = tr.find('span', {'class': 'offer_winename'})
            price = tr.find('span', {'class': 'offer_price'})
            seller_div = tr.find('div', {'itemprop': 'seller'})
            product_link = tr.find('a', {'class': 'offerblock'})
            
            seller_link_anchor = tr.find('a', {'title': 'Store information and contact details'})
            seller_location_div = tr.find('div', {'class': 'smallish'})
            seller_link = ''
            seller_name = ''
            seller_location = ''
            
            if seller_link_anchor and seller_location_div:
                seller_link = seller_link_anchor['href']
                seller_name = seller_link_anchor.text.strip()
                seller_location = seller_location_div.text.strip().replace('\n', ' ')
        
            if wine_name and price and product_link:
                wine_name = wine_name.text.strip()
                price = price.text.strip()
                product_link = product_link['href']
                seller_link = seller_link if (seller_link != '') else 'NA'
                seller_name = seller_name if (seller_name != '') else 'NA'
                seller_location = seller_location if (seller_location != '') else 'NA'
                
                # build list
                result_list.append({'wine_name': wine_name,
                                    'price': price,
                                    'seller_link': seller_link,
                                    'seller_name': seller_name,
                                    'seller_location': seller_location,
                                    'product_link': product_link})
        return result_list
        
    def _get_query_result_from_vivino(self, arg_query_str):
        req = urllib2.Request(arg_query_str, headers = dict_query_info.vivino_api['headers']) 
        con = urllib2.urlopen( req )
        soup = BeautifulSoup(con.read())
        list_div = soup.find('div', {'class': 'search-results-list'})
        if list_div is None:
            return []
        divs = list_div.find_all('div', {'class': 'wine-card'})
        if divs is None:
            return []
            
        # iterate list
        result_list = []
        for count, div in enumerate(divs):
            #
            mark_name = div.find('h3', {'class': 'winery semi header-small'}).text.strip()
            wine_name = div.find('h2', {'class': 'wine-name header-medium'}).text.strip()
            region = div.find('h4', {'class': 'origin semi header-smaller link-muted'}).text.strip().replace('\n', ' ') if div.find('h4', {'class': 'origin semi header-smaller link-muted'}) else 'NA'
            price_link = div.find('div', {'class': 'wine-thumbnail'}).find('a')['href']
            img_link = div.find('div', {'class': 'wine-thumbnail'}).find('a')['style']
            price_link = dict_query_info.vivino_api['base_url'] + price_link
            img_link = re.search('\'(.*)\'', img_link).group(1)
            rating_div = div.find('div', {'itemprop': 'aggregateRating'})
            rating = rating_div.find('span', {'itemprop': 'ratingValue'}).text.strip() if (rating_div and rating_div.find('span', {'itemprop': 'ratingValue'})) else 'NA'
            rating_count = rating_div.find('meta', {'itemprop': 'reviewCount'})['content'] if (rating_div and rating_div.find('meta', {'itemprop': 'reviewCount'})) else 'NA'
            # build result list
            result_list.append({'mark_name': mark_name,
                                'wine_name': wine_name,
                                'region': region,
                                'price_link': price_link,
                                'img_link': img_link,
                                'rating': rating,
                                'rating_count': rating_count})
                                
        return result_list
    
# configuration
dict_setting = Setting()
config = dict_setting.config_setting

# app
app = webapp2.WSGIApplication([
    webapp2.Route(r'/query/search_wine_info', WineQueryHandler, name='snooth')
], debug=True, config=config)

# log
logging.getLogger().setLevel(logging.DEBUG)