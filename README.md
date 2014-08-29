pyAppAnnie
==========

[AppAnnie](http://www.appannie.com) is a service for mobile apps analytics. Here is a tiny python wrapper for main AppAnnie API endpoints.

## Methods

Bold parameters are required.

### Meta

* **meta_regions**()
* **meta_categories**(market)

### Store

* **store_top**(market, countries, categories, device, feeds, ranks, date)

### Account

* **account_connections**(page)
* **account\_connections\_apps**(**acc_id**, page)
* *account\_in\_app\_purchase*(*acc\_id*, *app_id*, page)
* *account\_shared_apps*(page)
* *account\_sales*(*acc\_id*, break\_down, start\_date, end_date, currency, countries, page)

### Publisher

* *pub_top*(market, countries, categories, device, feeds, ranks, granularity, date)
* *pub\_downloads*(*pub\_id*, market, categories, countries, device, granularity, start\_date, end_date)
* *pub\_revenue*(*pub\_id*, market, categories, countries, device, granularity, start\_date, end_date)

### Application

* *app\_sales*(*app\_id*, *acc\_id*, break\_down, start\_date, end_date, currency, countries, page)
* *app_top*(market, countries, categories, device, feeds, ranks, granularity, date)
* *app_search*(*query*, market, countries, categories, device, feeds, granularity, date)
* *app\_details*(*app_id*, market)
* *app\_downloads*(*app\_id*, market, countries, device, granularity, start\_date, end_date)
* *app\_revenue*(*app\_id*, market, countries, device, granularity, start\_date, end_date)
