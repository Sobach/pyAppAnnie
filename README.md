pyAppAnnie
==========

[AppAnnie](http://www.appannie.com) is a service for mobile apps analytics. Here is a tiny 
python wrapper for main AppAnnie API endpoints.

## Quick start

Go to your AppAnnie [profile](https://www.appannie.com/account/api/key/) and generate 
your API key. Use it to initialize API class.

```Python
from pyappannie import API
from pprint import pprint
api_key = '### PUT YOUR SECRET KEY HERE ###'
api = API(api_key)
# Getting countries list
pprint(api.meta_regions())
# Searching for messengers in top (access to Intelligence API is required)
pprint(api.app_search('messenger', countries = 'US'))
```

## Methods

Bold parameters are required.

### Meta

* **meta_regions**()
* **meta_categories**(market)
* **meta_platforms**()
* **meta_currencies**()

### Store

* **store_top**(market, countries, categories, device, feeds, ranks, date)

### Account

* **account_connections**(page)
* **account\_connections\_apps**(**acc_id**, page)
* **account\_in\_app\_purchase**(**acc\_id**, **app_id**, page)
* **account\_shared_apps**(page)
* **account\_sales**(**acc\_id**, break\_down, start\_date, end_date, currency, countries, page)

### Publisher

* **pub_top**(market, countries, categories, device, feeds, ranks, granularity, date)
* **pub\_downloads**(**pub\_id**, market, categories, countries, device, granularity, start\_date, end_date)
* **pub\_revenue**(**pub\_id**, market, categories, countries, device, granularity, start\_date, end_date)

### Application

* **app\_sales**(**app\_id**, **acc\_id**, break\_down, start\_date, end_date, currency, countries, page)
* **app_top**(market, countries, categories, device, feeds, ranks, granularity, date)
* **app_search**(**query**, market, countries, categories, device, feeds, granularity, date)
* **app\_details**(**app_id**, market)
* **app\_downloads**(**app\_id**, market, countries, device, granularity, start\_date, end_date)
* **app\_revenue**(**app\_id**, market, countries, device, granularity, start\_date, end_date)
* **app\_ranks**(**app\_id**, market, start\_date, end\_date, interval, countries, categories, feeds, device)
* **app\_features**(**app\_id**, market, start\_date, end\_date, countries, page)
* **app\_reviews**(**app\_id**, **acc\_id**, start\_date, end\_date, countries, version, rating, page)
* **app\_ratings**(**app\_id**, market, page)
