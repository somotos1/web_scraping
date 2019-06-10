from flask import Flask
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():

    # Identify and activate the browser
    browser = init_browser()

    final_results = {}
    # Scrape the Mars Nasa Website for News articles
    # Set the url and use chromedriver to visit the url
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(2)

    html = browser.html
    # Use beautiful soup and set the parser to html
    soup = bs(html, 'html.parser')
    #   assign title to be = div where class = 'content-title' 
    news_title = soup.find('div', class_='content_title').text
    
    #     for each item in results, assign p to be = div where class = 'article-teaser-body' 
    news_p = soup.find('div', class_='article_teaser_body').text

    nasa_mars_news = {"title":news_title,"paragraph":news_p}

    browser.quit()

    final_results["nasa_mars_news"] = nasa_mars_news
# --------------------------------------------------------------------------------
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser('chrome', **executable_path, headless=True)
    # Set the url and use chrome webdriver to visit the webpage
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    time.sleep(2)

    # Parse through the html, find the item where the id='full_image' and click that item with chrome webdriver
    full_image = browser.find_by_id('full_image')
    full_image.click()
    time.sleep(2)

    # Find a link by 'more info' tag and click that item
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()
    time.sleep(2)

    # activate beautiful soup and select html parser 
    html = browser.html
    soup = bs(html, 'html.parser')
    # Find the image link and store it in a variable 
    jpl_image_url = soup.find('figure', class_='lede').a['href']

    # Include the beginning of the full webpage
    featured_image_url = 'https://www.jpl.nasa.gov' + jpl_image_url

    browser.quit()

    final_results["featured_image_url"] = featured_image_url

# --------------------------------------------------------------------------------
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser('chrome', **executable_path, headless=True)
    # Scrape the Mars Twitter Page
    # Set the url and use chrome webdriver to visit the webpage
    tw_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tw_url)
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    # Parse the html and find the first div tag where class = 'js-tweet-text-container'
    results = soup.find('div', class_='js-tweet-text-container')
    # Get the text in the results and store in a variable
    mars_weather = results.p.text

    browser.quit()

    final_results["mars_weather"] = mars_weather

# --------------------------------------------------------------------------------
    space_facts_url = 'https://space-facts.com/mars/'
    # Use pandas to read the html in the url, scrape the table and assign it to a variable
    table = pd.read_html(space_facts_url)
    # Select the first table
    table_df = table[0]
    # Change column names
    table_df.columns=["Title","Fact"]
    # Cnvert html to dictionary with pandas
    table_dict = table_df.to_dict(orient='records')
    # Insert into final results
    final_results["html_table"] = table_dict
    # print(final_results)
# --------------------------------------------------------------------------------

    # Scrape the USGS Astrogeology site

    driver = webdriver.Chrome()
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    driver.get(usgs_url)
    time.sleep(2)
    # Create empty list to hold dictionaries
    hemisphere_image_urls=[]

    loops = 4 # We know there are 4 images
    # Loop through the following while loops is greater than 0
    while loops > 0:
        # Create empty dictionary to save Title and Url
        d = {}
        # Use selenium to find the section where class name = 'description'
        parentElement = driver.find_elements_by_class_name('description')
        #  List comprehension; loop through the sections with class name 'description
        #  and obtain the element where class name = 'itemLink'
        urls = [x.find_element_by_class_name('itemLink') for x in parentElement]
        # Since python is zero based for indexing, decrement loops by one to select from urls list
        url = urls[loops - 1]
        # Click the selected url
        url.click()
        # Find Element With text Original. This contains the url we need
        image_element = driver.find_element_by_link_text('Sample')
        # Get the href and store image url in a variable
        image_url = image_element.get_attribute('href')
        # Find element where class name = title. This contains the image title
        title_element = driver.find_element_by_class_name('title')
        # Get the text and store it in a variable
        title = title_element.text
        # Add key-value pairs to dictionary for title and image url
        d["title"] = title
        d["image_url"] = image_url
        # Append dictionary to list
        hemisphere_image_urls.append(d)
        # Go back to previous page
        driver.execute_script("window.history.go(-1)")
        # Decrement loops by 1, to 3, and eventually 0 where the while loop will end
        loops -= 1
    # Print the list to check results
    
    final_results["hemisphere_image_urls"] = hemisphere_image_urls

    return final_results

r = scrape_info()
print(r)
