from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

def get_parsed_text():
    driver.get('https://m.blog.naver.com/stageinfo/?categoryNo=0&listStyle=post')    
    time.sleep(2)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    # ul_tags = soup.find_all('ul', {'class': ['list__aJqVF', 'list__bcW5n']})
    ul_tags = soup.find_all('div', {'class': ['content__zHIn1']})
    span_texts = []
    for ul_tag in ul_tags:
        span_tags = ul_tag.find_all('strong', {'class': 'title__yuIvy'})
        for span_tag in span_tags:
            span_texts.append(span_tag.text)
    return span_texts

if __name__ == '__main__':
    span_texts = get_parsed_text()
    for span_text in span_texts:
        print(span_text)


# post_name.txt 내용을 post_name 리스트에 저장
# post_name=[]
# with open('post_name.txt', 'r',encoding='utf-8') as f:
#     for line in f:
#         post_name.append(line.strip())  
