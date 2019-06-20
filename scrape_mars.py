def scrape():
    import os
    from bs4 import BeautifulSoup as bs
    import requests
    import pymongo
    from splinter import Browser
    import pandas as pd
    import time


    executable_path = {"executable_path": r"C:\Users\mrunm\GitLab\GWARL201902DATA3\01-Lesson-Plans\12-Web-Scraping-and-Document-Databases\2\Activities\07-Ins_Splinter\Solved\chromedriver.exe"}
    browser=Browser("chrome", **executable_path, headless=False)

    #NASA News
    url_nasa='https://mars.nasa.gov/news/'
    browser.visit(url_nasa)
    time.sleep(1)
    html=browser.html
    soup=bs(html,'html.parser')
    news_title=soup.find('div',class_="content_title").find('a').text
    news_p=soup.find('div',class_="article_teaser_body").text

    #JPL Mars Space
    url_img='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_img)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    html=browser.html
    soup=bs(html,'html.parser')
    img=soup.find('figure',class_="lede").a['href']
    featured_img_url=f"https://www.jpl.nasa.gov{img}"

    #Mars Weather
    url_twt='https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twt)
    time.sleep(1)
    html=browser.html
    soup=bs(html,'html.parser')
    mars_weather=soup.find('div',class_="js-tweet-text-container").find('p').text

    #Mars Facts
    url_fact='https://space-facts.com/mars/'
    tables=pd.read_html(url_fact)
    time.sleep(1)
    mars_df=tables[0]
    mars_df.columns=['Description','Value']
    mars_df.set_index('Description',inplace=True)
    mars_data=mars_df
    html_table = mars_data.to_html(header=False).replace('\n', '')
    

    #Mars Hemispheres
    url_astro='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_astro)
    time.sleep(1)
    html=browser.html
    soup=bs(html,'html.parser')
    results=soup.find_all('div',class_="item")
    hemisphere_image_urls=[]
    base_url='https://astrogeology.usgs.gov'
    
    for result in results:
        titles=result.find('h3').text
        link_to_fullsize=result.find('a',class_="itemLink product-item")['href']
        browser.visit(base_url+link_to_fullsize)
        time.sleep(1)
        link_pg_html=browser.html
        soup=bs(link_pg_html,'html.parser')
        img_url=base_url + soup.find('img',class_="wide-image")['src']
        hemisphere_image_urls.append({"Title":titles,"Image_url":img_url})

    browser.quit()
    
    mars_dict={
      "title_news":news_title,
      "news_desc":news_p,
      "featured_img":featured_img_url,
      "mars_weather":mars_weather,
      "mars_facts":html_table,
      "mars_hemisphers":hemisphere_image_urls
    }
    
    return mars_dict