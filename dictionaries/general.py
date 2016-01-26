'''
Created on Dec 24, 2014

@author: Alan Tai
'''

class Setting(object):
    """ general key and value pair """
    def __init__(self):
        
        # config. setting
        self.config_setting = {
                               'webapp2_extras.sessions': {'secret_key': 'b4RiUe~53!kGt3QSt3FYJTJ5-5&u90u1$%Y$%~e0.+54=954094309fewt3i-AqFHS$u2cNwOQGG',  # secret key is just a combination of random character which is better to be unguessable; user can create whatever they want
                                                           'cookie_name' : 'gogistics-winever-session',
                                                           'session_max_age' : 86400,
                                                           'cookie_args' : {'max_age' : 86400,
                                                                            'httponly' : True},} 
                               }
                               
class QueryInfo(object):
    """ """
    def __init__(self):
        # deafult setting of crawler
        self.wine_shops_urls = [{u"title" : u"K&L",                        u"link" : 'http://www.klwines.com'},
                                 {u"title" : u"BenchMarkWine",              u"link" : 'https://www.benchmarkwine.com'},
                                 {u"title" : u"WineBid",                    u"link" : 'http://www.winebid.com'},
                                 {u"title" : u"BelmontWine",                u"link" : 'http://www.belmontwine.com'},
                                 {u"title" : u"The Wine Club",              u"link" : 'http://www.thewineclub.com'},
                                 {u"title" : u"Aabalat Fine and Rare Wine", u"link" : "https://aabalat.com"},
                                 {u"title" : u"Rare Wine Co.",              u"link" : "http://www.rarewineco.com/fine-wines/"}]
        
        # query api
        self.snooth_api = { u'base_url' : u'http://api.snooth.com/wines/?akey=vs50x5xmuhowueopwoqlp7r5g0ik44acog3bwhpeylb1lf73&format=json',
                            u'default_ip' : u'67.188.149.11' }
                            
        self.wine_searcher_api = { u'base_url': u'http://www.wine-searcher.com/find/',
                                   u'reroute_url': 'http://leoninetechs.com/get_query_result',
                                   u'headers': {"Accept-Language": "en-US,en;q=0.8,fr;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2",
                                                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
                                                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                                "Referer": "http://wine.gogistics-tw.com",
                                                "Connection": "keep-alive" }}
                                                
        self.vivino_api = { u'base_url': u'https://www.vivino.com',
                            u'search_url': u'https://www.vivino.com/search?q=',
                            u'img_url': u'https:',
                            u'headers': {"Accept-Language": "en-US,en;q=0.8,fr;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2",
                                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
                                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                        "Referer": "http://wine.gogistics-tw.com",
                                        "Connection": "keep-alive" }}
                                                
                                                