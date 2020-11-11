from Crawler.LogIn import *
from Crawler.Helper import *

from datetime import date

# Define user agent
user_agent = "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
url = 'https://www.hkexnews.hk/sdw/search/searchsdw.aspx'

def main():

    # Create browser
    # browser ,_ = createBrowser(user_agent = user_agent, headless = '--headless')

    browser ,_ = createBrowser(user_agent = user_agent)

    # Browse url
    browser = getURL(browser, url)

    # Deinfe the date to search
    date_to_search = date(2019, 12, 11)
    
    # Define stock code
    stock_code = '00001'

    # Enter search keywords
    enter_search_kw(browser, stock_code, date_to_search)

    time.sleep(1)

    # Scrape data
    df = scraper(browser, stock_code, date_to_search)

    # Load data
    target_path = f'data\\{stock_code}-{date_to_search.strftime("%Y%m%d")}.csv'
    df.to_csv(target_path, index = False)

if __name__ == '__main__':
    main()


