from bs4 import BeautifulSoup
import requests
HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                           'Accept-Language': 'en-US, en;q=0.5'})

def extractname(url):
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")

    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        # print(title)
        Information=str(title)
        #print(Information)
        lines = Information.split("\n")
        non_empty_lines = [line for line in lines if line.strip() != ""]

        string_without_empty_lines = ""
        for line in non_empty_lines:
            string_without_empty_lines += line + "\n"

        Information=string_without_empty_lines
        i=Information.find("\">")
        j=i+3
        while(Information[j]!='<'):
            j+=1
        return Information[i+3:j]
    except AttributeError:

        return "NA"

    