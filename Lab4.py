import requests
from bs4 import BeautifulSoup
from queue import Queue
import threading
import time


def get_posts(url, queue):
    posts = []
    while True:
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        rr = soup.find_all('div', ['side-news', 'main-news', 'bottom-news'])
        for i in rr:
            items = i.find_all(['div', 'a'], ['item-image', 'item'])
            page_text = ''

            for item in items:
                title = item.find('div', {'class':'title'}).text
                try:
                    created = item.find('span', {'class':'created'}).text
                except AttributeError:
                    created = 'created = N/A'
                try:
                    content = item.find('div', {'class':'content'}).text
                except AttributeError:
                    content = 'content = N/A'
                try:
                    information = item.find('span', {'class':'information'}).text
                except AttributeError:
                    information = 'information = N/A'
                try:
                    announcement = item.find('span', {'class':'announcement'}).text
                except AttributeError:
                    announcement = 'announcement = N/A'
                try:
                    page = item.find_all('a', {'class':'page'})
                    for i in page:
                        page_text += ' ' + i.text
                except AttributeError:
                    page_text = 'page = N/A'

                if title not in posts:
                    posts.append(title)
                    queue.put({
                                'title':title,
                                'created':created,
                                'content':content,
                                'page':page_text,
                                'information':information,
                                'announcement':announcement
                             })
        time.sleep(100)


queue = Queue()
url = 'https://toipkro.ru/'
thread = threading.Thread(target=get_posts, args=(url, queue))
thread.start()
while True:
    posts = queue.get()
    if posts['information'] != 'information = N/A':
        print(posts['information'])
    if posts['announcement'] != 'announcement = N/A':
        print(posts['announcement'])
    print(posts['created'])
    print(posts['page'])
    print(posts['title'])
    print(posts['content'])
    print('\n')