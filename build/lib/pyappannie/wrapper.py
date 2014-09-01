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

def yesterday():
    return datetime.date.today() - datetime.timedelta(days = 1)
    
def q_transform(string):
    return ''.join(re.findall('[a-zA-Z]', string)).lower()
    
class AppAnnieAPI(object):
    DEFAULT_ENDPOINT = 'https://api.appannie.com/'

    def __init__(self, api_key, endpoint=DEFAULT_ENDPOINT):
        self.endpoint = endpoint
        self.api_key = api_key
                        
    def meta_regions(self):
        method = 'v1.1/meta/countries'
        return self._request(method)
    
    def meta_categories(self, market = 'google-play'):
        method = 'v1.1/meta/apps/{}/categories'.format(market)
        return self._request(method)
    
    def meta_platforms(self):
        method = 'v1/meta/platforms'
        return self._request(method)
        
    def meta_currencies(self):
        method = 'v1/meta/currencies'
        return self._request(method)

    def account_connections(self, page = 0):
        method = 'v1/accounts?page_index={}'.format(page)
        return self._request(method)
    
    def account_connections_apps(self, acc_id, page=0):
        method = 'v1/accounts/{}/apps?page_index={}'.format(acc_id, page)
        return self._request(method)
    
    def account_in_app_purchase(self, acc_id, app_id, page = 0):
        method = 'v1/{}/apps/{}/iaps?page_index={}'.format(acc_id, app_id, page)
        return self._request(method)
    
    def account_shared_apps(self, page = 0):
        method = 'v1/sharing/apps?page_index={}'.format(page)
        return self._request(method)
    
    def account_sales(self, acc_id, break_down = 'application+country+date', start_date = None, 
                      end_date = None, currency='USD', countries='WW', page=0):
        return self._get_sales('account', acc_id, None, break_down, start_date, end_date, currency, countries, page)

    def app_sales(self, app_id, acc_id, break_down = 'application+country+date', start_date = None, 
                      end_date = None, currency='USD', countries='WW', page=0):
        return self._get_sales('app', acc_id, app_id, break_down, start_date, end_date, currency, countries, page)
    
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

    def store_top(self, market = 'google-play', countries = 'WW', categories = 'OVERALL', 
                device = 'android', feeds = 'free paid grossing', ranks = 100, 
                date = yesterday().strftime('%Y-%m-%d')):
        return self._get_top('store', market, countries, categories, device, feeds, ranks, 
               None, date)
        
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
    
    def app_details(self, app_id, market = 'google-play'):
        method = 'v1.1/apps/{}/app/{}/details'.format(market, app_id)
        return self._request(method)
    
    def app_ranks(self, app_id, market = 'google-play', start_date = None, end_date = None,
                  interval = 'daily', countries = 'WW', categories = 'OVERALL',
                  feeds = 'free', device = 'android'):
        if market != 'google-play' and device == 'android':
            device = 'iphone'
        if not start_date:
            start_date = prevFirstDay().strftime('%Y-%m-%d')
        if not end_date:
            end_date = prevLastDay().strftime('%Y-%m-%d')
        method = 'v1.1/apps/{}/app/{}/ranks'.format(market, app_id)
        params = {'start_date':start_date, 'end_date':end_date, 'interval':interval, 
                  'countries':countries, 'category':categories, 'feed':feeds, 'device':device}
        return self._request(method, params)
    
    def app_features(self, app_id, market = 'google-play', start_date = None, end_date = None,
                     countries = 'WW', page = 0):
        if not start_date:
            start_date = prevFirstDay().strftime('%Y-%m-%d')
        if not end_date:
            end_date = prevLastDay().strftime('%Y-%m-%d')
        method = 'v1.1/apps/{}/app/{}/features'.format(market, app_id)
        params = {'start_date':start_date, 'end_date':end_date, 'countries':countries,
                  'page_index':page}
        return self._request(method, params)
    
    def app_reviews(self, app_id, acc_id, start_date = None, end_date = None, countries = 'WW',
                    version = 'all', rating = '5', page = 0):
        if not start_date:
            start_date = prevFirstDay().strftime('%Y-%m-%d')
        if not end_date:
            end_date = prevLastDay().strftime('%Y-%m-%d')
        method = 'v1/accounts/{}/apps/{}/reviews'.format(acc_id, app_id)
        params = {'start_date':start_date, 'end_date':end_date, 'countries':countries,
                  'page_index':page, 'version':version, 'rating':rating}
        return self._request(method, params)
    
    def app_ratings(self, app_id, market = 'google-play', page=0):
        method = 'v1.1/apps/{}/app/{}/ratings'.format(market, app_id)
        params = {'page_index':page}
        return self._request(method, params)
        
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

    def _get_sales(self, sales_for, acc_id, app_id, break_down, start_date, end_date, currency, countries, page):
        if sales_for == 'account':
            method = 'v1/accounts/{}/sales'.format(acc_d)
        elif sales_for == 'app':
            method = 'v1/accounts/{}/apps/{}/sales'.format(acc_id, app_id)
        if not start_date:
            start_date = prevFirstDay().strftime('%Y-%m-%d')
        if not end_date:
            end_date = prevLastDay().strftime('%Y-%m-%d')
        params = {'break_down':break_down, 'start_date':start_date, 'end_date':end_date, 
                  'currency':currency, 'countries':countries, 'page_index':page}
        return self._request(method, params)
                                     
    def _get_top(self, top_of, market, countries, categories, device, feeds, ranks, 
                granularity, date):
        if top_of == 'apps':
            method = 'v1.1/intelligence/apps/{}/ranking'.format(market)
        elif top_of == 'pubs':
            method = 'v1.1/intelligence/apps/{}/publisher-ranking'.format(market)
        elif top_of == 'store':
            method = 'v1.1/apps/{}/ranking'.format(market)
        
        if market == 'ios' and device == 'android':
            device = 'ios'
        if not date:
            date = prevLastDay().strftime('%Y-%m-%d')
        params = {'countries':countries, 'categories':categories, 'device':device,
                  'feeds':feeds, 'date':date}
        if top_of != 'store':
            params['granularity'] = granularity
        if ranks:
            params['ranks'] = ranks
        return self._request(method, params)

    def _get_history(self, history_of, feed, id, market, categories, countries, device, 
                    granularity, start_date, end_date):
        if history_of == 'pub':
            history_of = 'publisher'
        method = 'v1.1/intelligence/apps/{}/{}/{}/history'.format(market, history_of, id)
        
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