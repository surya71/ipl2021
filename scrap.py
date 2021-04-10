import requests
from bs4 import BeautifulSoup

def getLiveScore(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    result = requests.get(url,headers=headers)
    soup = BeautifulSoup(result.content,'html.parser')
    x = soup.find('div',class_='event')
    name = x.find_all('p',class_='name')
    score = x.find_all('span',class_='score')
    score_info = x.find_all('span',class_='score-info')
    status_text = x.find('div',class_='status-text').text
    livescore = {'name':name,'score':score,'score_info':score_info,'status_text':status_text}
    comment = soup.find_all('div',class_="match-comment-short-text")
    return livescore,comment
