from lxml import html
import requests
import yaml
from urlparse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from HTMLParser import HTMLParser

# custom py
from keyword_extractor import *

# function scrape controller
def scrape(url, data):
    if('pagination' in data or 'one_per_page' in data):
        return scrape_site(url, data)
    else:
        return scrape_page(url, data)

# function scrape multiple pages
def scrape_site(url, data):
    collect_links = False
    if('one_per_page' in data):
        collect_links = True
    if('list_all' in data):
        list_all = data['list_all']
        url += list_all
    next_page = ''
    if('pagination' in data):
        next_page = data['page_url']
    job_data = []
    pno = 0
    while True:
        cur_data = scrape_page(url, data, collect_links)
        if(len(cur_data) == 0):
            break
        else:
            job_data.extend(cur_data)
            if(next_page == ''):
                break
            pno += 1
            url = url + next_page.replace('[?]', str(pno))
            pno = int(pno)
    # if collect links, scrape each page again
    if(collect_links == True):
        sdata = []
        for link in job_data:
            cur_data = scrape_page(link, data)
            sdata.extend(cur_data)
        return sdata
    else:
        return job_data
        

        
# function scrape single page
def scrape_page(url, data, collect_links = False):
    if(data['js'] == True):
        driver = webdriver.PhantomJS()
        driver.get(url)
        html = driver.page_source
    else:
        page = requests.get(url)
        html = page.content
    soup = BeautifulSoup(html, 'lxml')
    if 'iframe' in data:
        iurl = soup.select(data['iframe'])[0]['src']
        page = requests.get(iurl)
        soup = BeautifulSoup(page.content, 'lxml')
    # collect links
    if(collect_links):
        links = []
        listing = soup.select(data['one_per_page']['wrapper'])
        for post in listing:
            link = post.select(data['one_per_page']['link'])[0]['href']
            if(not is_absolute(link)):
                parsed_uri = urlparse(url)
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                link = domain + link
            links.append(link)
        return links
    else:
        posts = []
        listing = soup.select(data['wrapper'])
        for post in listing:    
            title = post.select(data['title'])
            location = post.select(data['location'])
            description = post.select(data['description'])
            #print '**********************'
            #print get_all_text(title)
            #print get_all_text(location)
            #print get_all_text(description)
            #print '**********************'
            posts.append({'title': get_all_text(title), 'location':
                                                           get_all_text(location),
                          'description': get_all_text(description)})
        return posts

# function extract text
def get_all_text(lst):
    ret = ''
    for each in lst:
        ret += each.get_text().encode('utf-8')+' '
    return ret.strip()

def is_absolute(url):
    #return bool(urlparse.urlparse(url).netloc)
    return True

# get career urls
with open('urls.txt') as f:
    content = f.readlines()
content = [x.strip() for x in content] 

# load tpl details from config file
f = open('scraper-config.yml');
data_map = yaml.safe_load(f)
f.close()

for each in content:
    puri = urlparse(each)
    domain = '{uri.netloc}'.format(uri=puri)
    if domain in data_map:
        extracts = scrape(each, data_map[domain])
    else:
        print 'Domain: '+domain+' not found'
    # for each job post
    for each in extracts:
        keywords = extract_keywords(each['description']); 
        print keywords
        
