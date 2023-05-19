import random
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from requests import get
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
import datetime
import random
import linecache

USED_IPS = set()
MAX_IPS = 1000


def get_tor_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="1234qwer")
        controller.signal(Signal.NEWNYM)
        time.sleep(controller.get_newnym_wait())
        with get("https://ident.me", proxies={"http": "socks5://localhost:9050", "https": "socks5://localhost:9050"}) as response:
            return response.text.strip()

def reset_used_ips():
    global USED_IPS
    USED_IPS = set()

def open_url(url):    
    hostname="socks5://127.0.0.1"
    port="9050"
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % hostname + ":" + port) 
    user_agent = UserAgent().random
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('headless')
    service = Service('/usr/lib64/chromium-browser/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    print('📢 search naver')
    line_number = random.randint(1, len(open('post_name.txt',encoding='utf-8').readlines()))
    post_name = linecache.getline('post_name.txt', line_number).strip()
    driver.get('https://search.naver.com/search.naver?ie=UTF-8&query=%22'+post_name+'%22&sm=chr_hty')
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    print('📢 search naver complete')
    driver.find_element(By.CSS_SELECTOR, 'a[href*="blog.naver.com/stageinfo"]').click()
    print('📢 post load')
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    print('📢 post load complete')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('📢 scrooll down')
    wait=random.randint(60, 120)
    print('📢 wating : '+str(wait)+'sec')
    time.sleep(wait)
    driver.quit()

def get_post_url():
    #requests 로 https://m.blog.naver.com/stageinfo/?categoryNo=0&listStyle=post
    


if __name__=="__main__":
    while True:
        ip = get_tor_ip()
        while ip in USED_IPS:
            ip = get_tor_ip()
        USED_IPS.add(ip)
        print(f"📢 Current IP: {ip}")
        gmt_now = datetime.datetime.utcnow()
        kst_now = gmt_now + datetime.timedelta(hours=9)
        print(kst_now)
        try:
            open_url()
        except:
            pass
        end=random.randint(10,70)
        print(end)
        time.sleep(end)
