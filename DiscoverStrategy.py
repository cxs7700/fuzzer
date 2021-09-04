from urllib.parse import urlparse
from urllib.parse import urljoin
import sys
import mechanicalsoup
import http.cookiejar
from custom_auth import *
from options import *


def discover(browser, words, url, auth):
    print("Crawling and guessing pages...\n")
    cookies = browser.get_cookiejar()    
    domain = urlparse(url).netloc
    
    crawledUrls, inputList, guessedPages = discoverPages(browser, domain, url, words, auth)
    print("LINKS FOUND ON PAGE:")
    print("====================")
    print("\n".join(crawledUrls))
    print("====================")

    print("LINKS SUCCESSFULLY GUESSED:")
    print("====================")
    print("\n".join(guessedPages))
    print("====================")

    print("INPUT FORMS ON PAGES:")
    print("====================")
    print("\n".join(inputList))
    print("====================")
    
    print("COOKIES:")
    print("====================")
    cookieList = []
    for c in cookies:
        cookie = {"name": c.name, "value": c.value}
        cookieList.append(cookie)
    for cookie in cookieList:
        print(cookie['name'] + ": " + cookie['value'])
    print("====================")

def discoverPages(browser, domain, url, words, auth):
    guessed_pages = []
    possible_paths = []
    common_extensions = {'.txt', '.php', '.jsp', '.html'}
    common_words = open(words, "r").read().splitlines()
    
    crawledUrls = []
    inputList = []
    urlList = [url]
    
    while len(urlList) > 0:
        url = urlList.pop(0)
        
        # Finding all links
        if url not in crawledUrls:
            browser.open(url)
            crawledUrls.append(url)
            page = browser.get_current_page()
            if page is None:
                continue           
            raw_links = page.find_all('a', href=True)
            for url in raw_links:
                url_netloc = urlparse(browser.absolute_url(url['href'])).netloc
                if domain == url_netloc and (browser.absolute_url(url['href']) not in crawledUrls):
                    urlList.append(browser.absolute_url(url['href']))
                    
            
            # Finding form inputs
            forms = page.find_all('form')
            if forms is None:
                continue
            for form in forms:
                inputs = form.find_all('input')
                if inputs is not None:
                    for input in inputs:
                        if (input.has_attr('name')):
                            inputList.append(input['name'])
            
    # Guessing pages
    for w in common_words:
        for e in common_extensions:
            possible_paths.append("/" + w + e)
            
    for url in crawledUrls:
        for p in possible_paths:
            resp = browser.open(url + p)
        if (browser.get_current_page() is None) and (resp.status_code != 200):
            continue
        guessed_pages.append(url + p)
    
    return crawledUrls, inputList, guessed_pages
    

def logInDVWA(url, auth):
    username = auth["dvwa"]["username"]
    password = auth["dvwa"]["password"]
    security_level = "low"

    browser = mechanicalsoup.StatefulBrowser()

    o = urlparse(url)
    security_url = o.scheme + "://" + o.netloc + "/security.php"
    setup_url = o.scheme + "://" + o.netloc + "/setup.php"

    # Create database
    browser.open(setup_url)
    browser.select_form('form[action="#"]')
    browser.submit_selected()

    # Log in
    browser.open(url)
    browser.select_form('form[action="login.php"]')
    browser['username'] = username
    browser['password'] = password
    browser.submit_selected()

    # Set security level to low, then begin fuzzing
    browser.open(security_url)
    browser.select_form('form[method="POST"]')
    browser["security"] = security_level
    browser.submit_selected()
    
    print("Logged into DVWA.")

    browser.open(url)

    return browser
