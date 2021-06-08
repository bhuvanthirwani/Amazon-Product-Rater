import requests
from bs4 import BeautifulSoup
import time
from random import choice
from urllib.parse import urlparse
import re
from fake_useragent import UserAgent



# # to ignore SSL certificate errors
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# random user-agent
ua = UserAgent()


class amazon_product_review_scraper:
    
  def __init__(self, amazon_site, product_asin, sleep_time=1, start_page=1, end_page=None):
      
      # url
      self.url = "https://www." + amazon_site + "/dp/product-reviews/" + product_asin + "/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber={}"
      self.sleep_time = sleep_time
      self.reviews_dict = {"date_info":[], "name":[], "title":[], "content":[], "rating":[]}
      
      self.proxies = self.proxy_generator()        
      self.max_try = 10
      self.ua = ua.random
      self.proxy = choice(self.proxies)
      
      self.start_page = start_page
      if (end_page == None):
          self.end_page = self.total_pages()
      else:
          self.end_page = min(end_page, self.total_pages())
      

  #
  def total_pages(self):
      response = self.request_wrapper(self.url.format(1))
      soup = BeautifulSoup(response.text, 'html.parser')
      
      ## TODO if else        
      content = soup.find_all("div", {"data-hook": "cr-filter-info-review-rating-count"})
      total_reviews = int(content[0].find_all("span")[0].get_text("\n").strip().split(" ")[4].replace(",", ""))
      print ("Total reviews (all pages): {}".format(total_reviews), flush=True)
      return total_reviews



  # wrapper around request package to make it resilient
  def request_wrapper(self, url):
      
      while (True):
          # amazon blocks requests that does not come from browser, therefore need to mention user-agent
          response = requests.get(url, verify=False, headers={'User-Agent': self.ua}, proxies=self.proxy)
          
          # checking the response code
          if (response.status_code != 200):
              raise Exception(response.raise_for_status())
          
          # checking whether capcha is bypassed or not (status code is 200 in case it displays the capcha image)
          if "api-services-support@amazon.com" in response.text:
              
              if (self.max_try == 0):
                  raise Exception("CAPTCHA is not bypassed")
              else:
                  time.sleep(self.sleep_time)
                  self.max_try -= 1
                  self.ua = ua.random
                  self.proxy = choice(self.proxies)
                  continue
              
          self.max_try = 5
          break
          
      return response

  # random proxy generator
  def proxy_generator(self):
      proxies = []
      response = requests.get("https://sslproxies.org/")
      soup = BeautifulSoup(response.content, 'html.parser')
      proxies_table = soup.find(id='proxylisttable')
      for row in proxies_table.tbody.find_all('tr'):
          proxies.append({
              'ip':   row.find_all('td')[0].string,
              'port': row.find_all('td')[1].string
          })

      proxies_lst = [{'http':'http://'+proxy['ip']+':'+proxy['port']} for proxy in proxies]
      return proxies_lst
# SCRAPE THE REVIEWS FOR THE LINK FROM USER
def info(link_user):
#   link = input("Enter the url for your product: ")
  link = link_user
  domain = urlparse(link).netloc
  website = '.'.join(domain.split('.')[1:])
  ind = link.find('/dp')
  id = link[ind+4:ind+14]
  review_scraper = amazon_product_review_scraper(amazon_site=website, product_asin=id, start_page=1, end_page=10)
  total_reviews = review_scraper.total_pages()
  return total_reviews



