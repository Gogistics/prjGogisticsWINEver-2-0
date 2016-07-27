# -*- coding: utf-8 -*-
'''
Created on Dec 24, 2014

@author: Alan Tai
'''
from handlers.webapp2_auth import BaseHandler
from dictionaries.general import Setting
import jinja2, webapp2, logging

# jinja environment
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('static/templates'))

# dict
dict_setting = Setting()

class FrontPageRouter(BaseHandler):
    def get(self):
        """ front page """
        template_values = {}
        template_values.update({'title' : 'Welcome to WINEver'})
        self.render_template("/front.html", template_values)
        
class IndexPageRouter(BaseHandler):
    def get(self):
        """ index page """
        template_values = {}
        template_values.update({"title" : "WINEver"})
        self.render_template("/index.html", template_values)
        
class LogsMonitorRouter(BaseHandler):
    def get(self):
        """ index page """
        template_values = {}
        template_values.update({"title" : "Scalyr"})
        self.render_template("/logs_monitor.html", template_values)
    
# configuration
config = dict_setting.config_setting

# app
app = webapp2.WSGIApplication([
    webapp2.Route(r'/', FrontPageRouter, name='front_page'),
    webapp2.Route(r'/base/index', IndexPageRouter, name='index_page'),
    webapp2.Route(r'/base/logs_monitor', LogsMonitorRouter, name='logs_monitor')
], debug=True, config=config)

# log
logging.getLogger().setLevel(logging.DEBUG)