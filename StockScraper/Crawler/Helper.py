import time
import pandas as pd
import numpy as np
import json
import psycopg2
import psycopg2.extras as extras

def calendar_click(browser, to_search, class_name):
    
    try:
        calendar_element = browser.find_element_by_class_name(class_name)
        
        for calendar in calendar_element.find_elements_by_tag_name('li'):
            if calendar.text.strip() == to_search:
                
                calendar.click()

        time.sleep(2)
        
    except Exception as e:
        print(e)

def enter_search_kw(browser, stock_code, date_to_search):

    year_to_search = str(date_to_search.year)
    month_to_search = str(date_to_search.month)
    day_to_search = str(date_to_search.day)

    # Click Calendar to open calendar
    browser.find_element_by_id('txtShareholdingDate').click()
    time.sleep(2)

    # Select the correct year, month and day
    calendar_click(browser, year_to_search, 'year')
    calendar_click(browser, month_to_search, 'month')
    calendar_click(browser, day_to_search, 'day')
    time.sleep(1)

    # Click Calendar to confirm the selected date
    browser.find_element_by_id('txtShareholdingDate').click()

    # Set Stock Code
    browser.find_element_by_name('txtStockCode').send_keys(stock_code)
    time.sleep(1)

    # Click Search
    browser.find_element_by_id('btnSearch').click()
    time.sleep(1)

# Scrape 市場中介者/願意披露的投資者戶口持有人的紀錄 on the page
def scraper(browser, stock_code, date_to_search):

    # Get search result table
    search_table = browser.find_element_by_class_name('search-details-table-container').find_element_by_tag_name('table')
    
    # Get column_name
    column_name = [col.text for col in search_table.find_elements_by_tag_name('th')]
    
    # Get Search body
    search_body = search_table.find_element_by_tag_name('tbody')
    
    # Get Search result data
    data = np.array([[cell.text for cell in row.find_elements_by_class_name('mobile-list-body')] for row in search_body.find_elements_by_tag_name('tr')])

    # Convert data to DataFrame with column
    df = pd.DataFrame(data, columns = column_name)
    
    # Add search stock data and date_to_search
    df['stock_code'] = stock_code
    df['report_date'] = date_to_search
    
    return df

def get_stock_codes(path):
    """
        Read Json file
        return a list of stock cod 
    """
    with open(path, 'r') as f:
        stock_dict = json.load(f)
        
    return list(stock_dict.values())
    
def load_data(df, params, col, table_col):

    # Preprocess data
    df = process_data(df)

    # Prepare Loading data tuples
    tuples = [tuple(x) for x in df[col].to_numpy()]

    # Prepare Insert sql statement
    table_col = ','.join(table_col)
    query  = "INSERT INTO %s(%s) VALUES %%s" % ('stock.portfolio', table_col)

    # Load data to postgres
    with psycopg2.connect(**params) as conn:
        cur = conn.cursor()
        extras.execute_values(cur, query, tuples)


def process_data(df):

    try:
        # Convert Shareholding to float
        df['Shareholding'] = df['Shareholding'].apply(lambda x: float(x.replace(',','')))
        df['Percentage'] = df['% of the total number of Issued Shares/ Warrants/ Units'].apply(lambda x: float(x.replace('%','')) / 100)
        df['stock_code'] = df['stock_code'].apply(lambda x: ('00000' + str(x))[-5:])
        return df
    except Exception as e:
        print(e)
        return None