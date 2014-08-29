#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import datetime
import re

def prevLastDay():
    today = datetime.date.today()
    first = datetime.date(day=1, month=today.month, year=today.year)
    return first - datetime.timedelta(days=1)

def prevFirstDay():
    l_day = prevLastDay()
    return datetime.date(day = 1, month=l_day.month, year = l_day.year)

def q_transform(string):
    return ''.join(re.findall('[a-zA-Z]', string)).lower()
    
class AppAnnieAPI(object):
    DEFAULT_ENDPOINT = 'https://api.appannie.com/v1.1/'

    def __init__(self, api_key, endpoint=DEFAULT_ENDPOINT):
        self.endpoint = endpoint
        self.api_key = api_key
                        
    def meta_regions(self):
        method = 'meta/countries'
        return self._request(method)
    
    def meta_categories(self, market = 'google-play'):
        method = 'meta/apps/{}/categories'.format(market)
        return self._request(method)
    
    def app_top(self, market = 'google-play', countries = 'WW', categories = 'OVERALL', 
                device = 'android', feeds = 'free paid grossing', ranks = 100, 
                granularity = 'daily', date = None):
        return self._get_top('apps', market, countries, categories, device, feeds, ranks, 
               granularity, date)

    def pub_top(self, market = 'google-play', countries = 'WW', categories = 'OVERALL', 
                device = 'android', feeds = 'free paid grossing', ranks = 100, 
                granularity = 'daily', date = None):
        return self._get_top('pubs', market, countries, categories, device, feeds, ranks, 
               granularity, date)
        
    def app_search(self, query, market = 'google-play', countries = 'WW', categories = 'OVERALL',
                   device = 'android', feeds = 'free paid grossing', granularity = 'monthly',
                   date = None):
        response = self.app_top(market = market, countries = countries, 
                                categories = categories, device = device, feeds = feeds,
                                ranks = None, granularity = granularity, date = date)
        print len(response['list'])
        response['query'] = query
        query = q_transform(query)
        result = []
        for app in response['list']:
            if query in q_transform(app['company_name']) or\
               query in q_transform(app['parent_company_name']) or\
               query in q_transform(app['product_franchise_name']) or\
               query in q_transform(app['product_name']) or\
               query in q_transform(app['publisher_name']) or\
               query in q_transform(app['unified_product_name']):
                result.append(app)
        response['list'] = result
        return response
               
    def app_downloads(self, app_id, market = 'google-play', countries = 'WW', 
                    device = None, granularity = 'daily',
                    start_date = None, end_date = None):
        return self._get_history('app', 'downloads', app_id, market, None, countries, device, 
                                 granularity, start_date, end_date)

    def app_revenue(self, app_id, market = 'google-play', countries = 'WW', 
                    device = None, granularity = 'daily',
                    start_date = None, end_date = None):
        return self._get_history('app', 'revenue', app_id, market, None, countries, device, 
                                 granularity, start_date, end_date)

    def pub_downloads(self, pub_id, market = 'google-play', categories = 'OVERALL',
                    countries = 'WW', device = None, granularity = 'daily',
                    start_date = None, end_date = None):
        return self._get_history('pub', 'downloads', pub_id, market, categories, countries, 
                                 device, granularity, start_date, end_date)

    def pub_revenue(self, pub_id, market = 'google-play', categories = 'OVERALL',
                    countries = 'WW', device = None, granularity = 'daily',
                    start_date = None, end_date = None):
        return self._get_history('pub', 'revenue', pub_id, market, categories, countries, 
                                 device, granularity, start_date, end_date)
    
    def _get_top(self, top_of, market, countries, categories, device, feeds, ranks, 
                granularity, date):
        if top_of == 'apps':
            top_of = 'ranking'
        elif top_of == 'pubs':
            top_of = 'publisher-ranking'
        method = 'intelligence/apps/{}/{}'.format(market, top_of)
        if market == 'ios' and device == 'android':
            device = 'ios'
        if not date:
            date = prevLastDay().strftime('%Y-%m-%d')
        params = {'countries':countries, 'categories':categories, 'device':device,
                  'feeds':feeds, 'granularity':granularity, 'date':date}
        if ranks:
            params['ranks'] = ranks
        return self._request(method, params)

    def _get_history(self, history_of, feed, id, market, categories, countries, device, 
                    granularity, start_date, end_date):
        if history_of == 'pub':
            history_of = 'publisher'
        method = 'intelligence/apps/{}/{}/{}/history'.format(market, history_of, id)
        
        if not device:
            if market == 'google-play':
                device = 'android'
            else:
                device = 'all'
        if not start_date:
            start_date = prevFirstDay().strftime('%Y-%m-%d')
        if not end_date:
            end_date = prevLastDay().strftime('%Y-%m-%d')
        params = {'countries':countries, 'feeds':feed, 'device':device,
                  'granularity':granularity, 'start_date':start_date,
                  'end_date':end_date}
        if history_of == 'publisher':
            params['categories'] = categories
        return self._request(method, params)

    def _request(self, method, params = {}):
        response = requests.get(self.endpoint + method, 
                                headers = {'Authorization':'Bearer {}'.format(self.api_key),
                                           'Accept':'application/json'},
                                params = params
                                )
        response = response.json()
        if response['code'] == 200:
            return response
        else:
            raise AppAnnieError(response)
        
class AppAnnieError(Exception):
    def __init__(self, value = {'error':'', 'code':0}):
        self.value = value
        if self.value['code'] == 400:
            self.value['reason'] = 'Bad Request'
        elif self.value['code'] == 401:
            self.value['reason'] = 'Unauthorized access'
        elif self.value['code'] == 403:
            self.value['reason'] = 'Forbidden'
        elif self.value['code'] == 404:
            self.value['reason'] = 'Not found'
        elif self.value['code'] == 405:
            self.value['reason'] = 'HTTP method is not supported'
        elif self.value['code'] == 429:
            self.value['reason'] = 'Rate limit exceeded'
        elif self.value['code'] == 500:
            self.value['reason'] = 'Internal service error'
        elif self.value['code'] == 503:
            self.value['reason'] = 'Service unavailable due to maintenance'
        else:
            self.value['reason'] = 'Something went wrong'

    def __str__(self):
        return '[{}] {}'.format(self.value['reason'], self.value['error'])