from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time, random

def createBrowser(chrome_options = ChromeOptions(), download_dir = None, **kwargs):
    """
        This function takes several arguments and return a instance of Chrome agent
        created by selenium
        
        >> chrome_options: default a new ChromeOptions instance; a existing chrome_options can be used in this function
        
        >> executable_path: directory pointing to your chromedriver
        
        -- Some important kwargs:
        >> incognito: '--incognito' or '--normal', if incognito is set to '--incognito', open private mode 
                      if incognito is set to '--normal', else, it wont open private mode, default incognito is set to '--incognito'

        >> disable_extensions: '--disable-extensions' or '--enable-extensions', disable chrome extension if '--disbale-extension' is set, of which 
                              they might affect the performance of chrome agent crawling target website, 
                              default disable_extensions is set to '--disable-extensions'

        >> user_agent: string, a descriptive string to mimick a normal user_agent
                       in the Chrome agent, default: empty_string
        ...
        Others argument, please refer to selenium doc
        
        E.g. you can specify --headless argument like the following:
            headless = "--headless"
    """
    # Check whether incognito, disable-extension and user-agent is in kwargs
    # if not, set up default value for those params
    try:
        if "incognito" not in kwargs.keys():
            print(">> 'incognito' not found in keyword arguments")
            print(">> Default: Private mode is set in Chrome agent")
            kwargs['incognito'] = '--incognito'
            
        elif kwargs['incognito'] == '--normal':
            print(">> '--normal' is found in the key")
            del kwargs['incognito']
            
        else:
            print(">> 'incognito is set in keyword arguments'")
    except:
        print(">> 'incognito' Checking Error.")
        return None, None
    
    # disable-extension
    try:
        if "disable_extensions" not in kwargs.keys():
            print(">> 'disable_extensions' not found in keyword arguments")
            print(">> Default: Chrome agent is disabled its extensions")
            kwargs['disable_extensions'] = '--disable-extensions'
            
        elif kwargs['disable_extensions'] == '--enable-extensions':
            print(">> '--enable-extensions is found in the key")
            del kwargs['disable_extensions']
            
        else:
            print(">> 'disable_extensions is set in keyword arguments'")
    except:
        print(">> 'disable_extensions' Checking Error")
        return None, None
    
    # Add each arguments in kwargs to chrome_options
    for key, arg in kwargs.items():
        
        try:
            print(">> {key} is added to chrome_options ".format(key = key))
            chrome_options.add_argument(arg)
        except:
            print(">> Warning: chrome_options cannot add {key} argument".format(key = key))
    
    #  Create Chrome agent
    browser = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
    
    return browser, chrome_options

def enable_download_in_headless_chrome(driver, download_dir):
    """
    there is currently a "feature" in chrome where
    headless does not allow file download: https://bugs.chromium.org/p/chromium/issues/detail?id=696481
    This method is a hacky work-around until the official chromedriver support for this.
    Requires chrome version 62.0.3196.0 or above.
    """

    # add missing support for chrome "send_command"  to selenium webdriver
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    command_result = driver.execute("send_command", params)
    print("response from browser:")
    for key in command_result:
        print("result:" + key + ":" + str(command_result[key]))

    return driver

def getURL(browser, url, window_size = (1900, 700), window_position = (0,0)):
    """
        This function is a url crawler. brower is the web agent created by createBrowser previously. 
        This function should follow by the createBrowser
        
        Input:
            browser: web agent created by createBrowser
            url: The target url that web agent will browse
            
        Remarks:
            1. Currently, only get method is supported
    """

    # Set up window size and position
    try:
        # window position
        handler = 'window_position'
        browser.set_window_position(window_position[0],window_position[1])
        
        # window size
        handler = 'window_size'
        browser.set_window_size(window_size[0], window_size[1])
    except:
        print(f'>> Error: {handler} failed to set')
        return browser
        
    
    # Get Url
    try:
        browser.get(url)
    except:
        print(f'>> Error: Browser cannot get {url}')
        return browser
    
    print(f'>> browser response: Get {browser.current_url}')
    
    return browser

