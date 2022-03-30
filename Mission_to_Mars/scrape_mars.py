from flask import Flask
import pymongo

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

@app.route("/scrape")
def scrape():

    import requests
    import pandas as pd
    from splinter import Browser
    from bs4 import BeautifulSoup
    from webdriver_manager.chrome import ChromeDriverManager


    # In[2]:


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[3]:


    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[ ]:


    print(soup)


    # In[ ]:


    results = soup.find('div', class_='container')
    print(results)


    # In[10]:


    for result in results:
        title = soup.find('div', class_='content_title')
        article = soup.find('div', class_='article_teaser_body')

    print(title.text)
    print(article.text)


    # In[12]:


    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[ ]:


    print(soup)


    # In[ ]:


    results = soup.find('div', class_='header')
    print(results)


    # In[19]:


    for result in results:
        image = soup.find('img', class_='headerimage fade-in')
    print(image)

    src = image.get('src')

    featured_image_url = url +"/" + src 
    print(featured_image_url)


    # In[20]:


    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[ ]:


    print(soup)


    # In[ ]:


    results = soup.find('table', class_='table table-striped')
    print(results)


    # In[32]:


    name_of_rows = results.find_all('th', scope='row')
    row_info = results.find_all('td')

    rows = []
    info = []

    for row in name_of_rows:
        rows.append(row.text)

    for line_info in row_info:
        info.append(line_info.text)

    #print(rows)
    #print(info)

    #fixing tab issue
    for x in range(len(info)):
        info[x] = info[x].replace('\t', '')

    print(rows)
    print(info)


    # In[33]:


    mars_facts = pd.DataFrame({
        'Mars Planet Profile': rows,
        "": info
    })
    mars_facts


    # In[34]:


    mars_facts.to_html("Mars_Dataframe.html")


    # In[48]:


    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[ ]:


    print(soup)


    # In[ ]:


    results = soup.find_all('div', class_='item')
    print(results)


    # In[51]:


    hempisphere_full_name = []
    hempisphere_name = []

    for result in results:
        hempisphere_name.append(result.find('a', class_= 'itemLink').get('href'))
        hempisphere_full_name.append(result.find('h3').text.rsplit(' ',1)[0])

    print(hempisphere_name)
    print(hempisphere_full_name)


    # In[59]:


    image_links = []

    for hemisphere in hempisphere_name:
        hemisphere_urls = url + hemisphere
        browser.visit(hemisphere_urls)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        #print(hemisphere_urls)

        downloads = soup.find('div', class_='downloads')
        #print(downloads)
        href_link = downloads.find('a', target='_blank').get('href')
        #print(href_link)
        hemi_images = url + href_link
        image_links.append(hemi_images)
    print(image_links)


    # In[60]:


    hemisphere_image_urls = []

    for x in range(len(hempisphere_name)):
        hemisphere_dictionary = {
            'title': hempisphere_full_name[x],
            'img_url': image_links[x]
        }
        hemisphere_image_urls.append(hemisphere_dictionary)

    hemisphere_image_urls


    # In[ ]:
    
    scraped_data = {
        "title": title.text,
        "article": article.text,
        "featured_image":featured_image_url,
        "table": mars_facts,
        'hemispheres': hemisphere_image_urls
    }
    return scraped_data
db = client.scrapedDB
scrape_results = db.scrape_results.find()
db.scrape_results.insert_one(scrape())

if __name__ == '__main__':
    app.run(debug=True)
    