from Crawler.LogIn import *
from Crawler.Helper import *

import os
from datetime import date
from datetime import timedelta
import random

# Define user agent
user_agent = "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
url = 'https://www.hkexnews.hk/sdw/search/searchsdw.aspx'
stock_list_path = './reference/ListOfStock.json'

col = ['Participant ID', 'Name of CCASS Participant\n(* for Consenting Investor Participants )',
       'Address', 'Shareholding','Percentage','stock_code','report_date']
table_col = ['participant_id', 'name_of_ccass_participant', 'address', 'shareholding', 'percentage', 'stock_code', 'report_date']
params = {
    'dbname':'stock',
    'host':'localhost',
    'port': 5432,
    'user':'postgres',
    'password':'postgres'
}

def main():

    # Define stock code
    stock_code_list = get_stock_codes(stock_list_path)

    # Execute batch Scrape
    batch_scrape(stock_code_list[:2])

def batch_scrape(stock_code_list, batch_size = 10):

    if stock_code_list:

        # Define batch_size and active/ inactive list
        batch_size = min([batch_size, len(stock_code_list)])
        active_list = stock_code_list[:batch_size]
        inactive_list = stock_code_list[batch_size:]

        # Random Shuffle
        random.shuffle(active_list)

        # Execute main_crawler for active_list
        main_crawler(active_list)

        # Break time
        time.sleep(random.randint(2,60))

        if inactive_list:
            
            # Recursive Loop
            batch_scrape(inactive_list)
        else:
            print('End of loop')

def main_crawler(stock_code_list):

    # Create browser
    browser ,_ = createBrowser(user_agent = user_agent, headless = '--headless')
    # browser ,_ = createBrowser(user_agent = user_agent)

    # Browse url
    browser = getURL(browser, url)

    # Deinfe the date to search
    date_to_search = date.today() - timedelta(1)

    for stock_code in stock_code_list:
        print(f'Start Scrape stock code: {stock_code}')
        # Enter search keywords
        enter_search_kw(browser, stock_code, date_to_search)

        time.sleep(1)

        # Scrape data
        df = scraper(browser, stock_code, date_to_search)

        # Load data
        load_data(df, params, col, table_col)

    browser.close()


if __name__ == '__main__':
    main()


