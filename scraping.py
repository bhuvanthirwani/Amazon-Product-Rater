import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time
import math
import string
from tqdm.auto import tqdm
from random import choice
from urllib.parse import urlparse
import re
import nltk
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from fake_useragent import UserAgent

#nltk.data.path.append('./nltk_data/')

#LOADING WEIGHTS FOR MODEL
LSTM=load_model('./model/LSTM.h5')
with open('./model/tokenizer.pickle', 'rb') as handle:
    tokenizer1 = pickle.load(handle)
nltk.download('punkt')
#WEB SCRAPING
# to ignore SSL certificate errors
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
        global no_of_reviews
        response = self.request_wrapper(self.url.format(1))
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ## TODO if else        
        content = soup.find_all("div", {"data-hook": "cr-filter-info-review-rating-count"})
        total_reviews = int(content[0].find_all("span")[0].get_text("\n").strip().split(" ")[4].replace(",", ""))
        no_of_reviews = total_reviews
        print ("Total reviews (all pages): {}".format(total_reviews), flush=True)
        
        total_pages = math.ceil(total_reviews/10)
        return total_pages

 
    # MAIN FUNCTION
    def scrape(self):

        
        print ("Total pages: {}".format(self.end_page - self.start_page+1), flush=True)
        print ("Start page: {}; End page: {}".format(self.start_page, self.end_page))
        #print ()
        print ("Started!", flush=True)

        for page in tqdm(range(self.start_page, self.end_page+1)):
            self.page_scraper(page)
            #
            time.sleep(self.sleep_time)

        #print ("Completed!")

        # returning df
        return pd.DataFrame(self.reviews_dict)

    
    # page scrapper
    def helper(self, content, tag, parameter_key, parameter_value):
        attribute_lst = []
        attributes = content.find_all(tag, {parameter_key: parameter_value})
        for attribute in attributes:
            attribute_lst.append(attribute.contents[0])
        return attribute_lst

    def page_scraper(self, page):
        
        try:

            response = self.request_wrapper(self.url.format(page))   

            # parsing content
            soup = BeautifulSoup(response.text, 'html.parser')
            ## reviews section
            reviews = soup.findAll("div", {"class":"a-section review aok-relative"})
            ## parsing reviews section
            reviews = BeautifulSoup('<br/>'.join([str(tag) for tag in reviews]), 'html.parser')

            ## 1. title
            titles = reviews.find_all("a", class_="review-title")
            title_lst = []
            for title in titles:
                title_lst.append(title.find_all("span")[0].contents[0])

            ## 2. name
            name_lst = self.helper(reviews, "span", "class", "a-profile-name")

            ## 3. rating
            ratings = reviews.find_all("i", {"data-hook":"review-star-rating"})
            rating_lst = []
            for rating in ratings:
                rating_lst.append(rating.find_all("span")[0].contents[0])

            ## 4. date
            date_lst = self.helper(reviews, "span", "data-hook", "review-date")   

            ## 5. content
            contents = reviews.find_all("span", {"data-hook":"review-body"})
            content_lst = []
            for content in contents:
                text_ = content.find_all("span")[0].get_text("\n").strip()
                text_ = ". ".join(text_.splitlines())
                text_ = re.sub(' +', ' ', text_)
                content_lst.append(text_)

            # adding to the main list
            self.reviews_dict['date_info'].extend(date_lst)
            self.reviews_dict['name'].extend(name_lst)
            self.reviews_dict['title'].extend(title_lst)
            self.reviews_dict['content'].extend(content_lst)
            self.reviews_dict['rating'].extend(rating_lst)

        except:
            print ("Not able to scrape page {} (CAPTCHA is not bypassed)".format(page), flush=True)
    
    
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
def info(link_user,x):
#   link = input("Enter the url for your product: ")
  link = link_user
  domain = urlparse(link).netloc
  website = '.'.join(domain.split('.')[1:])
  ind = link.find('/dp')
  id = link[ind+4:ind+14]

  
  review_scraper = amazon_product_review_scraper(amazon_site=website, product_asin=id, start_page=1, end_page=x)
  reviews_df = review_scraper.scrape()
  return reviews_df


#PROCESSING

def remove_url(text):
     url=re.compile(r"https?://\S+|www\.\S+")
     return url.sub(r" ",text)

def remove_html(text):
  cleanr = re.compile('<.*?>')
  return cleanr.sub(r" ",text)

def remove_num(texts):
   output = re.sub(r'\d+', '', texts)
   return output

def remove_punc(text):
   table=str.maketrans(' ',' ',string.punctuation)
   return text.translate(table)

nltk.download('stopwords')
from nltk.corpus import stopwords
stop=set(stopwords.words("english"))
   
def remove_stopword(text):
   text=[word.lower() for word in text.split() if word.lower() not in stop]
   return " ".join(text)

def Stemming(text):
   stem=[]
   from nltk.corpus import stopwords
   from nltk.stem import SnowballStemmer
   #is based on The Porter Stemming Algorithm
   stopword = stopwords.words('english')
   snowball_stemmer = SnowballStemmer('english')
   word_tokens = nltk.word_tokenize(text)
   stemmed_word = [snowball_stemmer.stem(word) for word in word_tokens]
   stem=' '.join(stemmed_word)
   #print(stem)
   return stem


max_length=100
vocab_size=12000
embedding_dim=64
trunc_type="post"
oov_tok="<OOV>"
padding_type="post"


#CALCULATE REVIEWS
def Review(sentence):
   sequences = tokenizer1.texts_to_sequences(sentence)
   padded = pad_sequences(sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

   prob=LSTM.predict(padded)
   if prob>=0.8:
     return 5
   elif prob>=0.6:
     return 4
   elif prob>=0.4:
     return 3 
   elif prob>=0.2:
     return 2   
   else:
     return 1


def Estimate(link_user,x):
  a = info(link_user,x)
  a = a['content']
  b = a.tolist()
  g = len(b)
  dataset = pd.DataFrame({'text':b})
  test = dataset
  test['number_of_words'] = test['text'].str.lower().str.split().apply(len)
  test['text']=test.text.map(lambda x:remove_url(x))
  test['text']=test.text.map(lambda x:remove_html(x))
  test['text']=test.text.map(lambda x:remove_punc(x))
  test['text']=test['text'].map(remove_num)
  test['text']=test.text.map(lambda x:remove_url(x))
  test['text']=test['text'].map(Stemming)
  word_index = tokenizer1.word_index

  testing_sequences = tokenizer1.texts_to_sequences(test['text'])
  testing_padded = pad_sequences(testing_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

  A=[]
  for index, row in dataset.iterrows():
      l = []
      l.append(row['text'])
      A.append(Review(l))
  print("The Product rating on the basis of latest reviews:-->",sum(A)/g)
  return sum(A)/g
# Estimate()