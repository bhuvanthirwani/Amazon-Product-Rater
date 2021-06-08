from bs4 import BeautifulSoup
import requests
HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                           'Accept-Language': 'en-US, en;q=0.5'})

def extract(url):
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")

    try:
        title = soup.find("div", attrs={"id": 'imgTagWrapperId'})
        # print(title)
        Information=str(title)
        #print(Information)
        i=Information.find("'{\"")
        j=i+3
        while(Information[j]!='"'):
            j+=1
        return Information[i+3:j]
    except AttributeError:

        return "NA"

    