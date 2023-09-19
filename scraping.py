import requests
from bs4 import BeautifulSoup

i=10

roman= []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

page = requests.get('https://ninjanovel.com/book/an-understated-dominance-by-marina-vittori-free-online/chapter-1/',headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')
block = soup.find('div',class_='text-left').get_text()
next = soup.find('div',class_='nav-next')

print(block)

next_url = next.find('a', href=True)['href']
#print(next_url)


while next_url is not None:
    page = requests.get(next_url,headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    block = soup.find('div',class_='text-left').get_text()
    print(block)
    
    next = soup.find('div',class_='nav-next')
    next_url = next.find('a', href=True)['href']
    #print(next_url)
