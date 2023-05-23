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
COUNT = 0

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

def open_url():
    user_agent=UserAgent().random
    service = Service('/usr/lib64/chromium-browser/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--proxy-server=%s:%s' % ('socks5://127.0.0.1', '9050'))
    driver = webdriver.Chrome(service=service, options=options)
    line_number = random.randint(1, len(open('post_name.txt',encoding='utf-8').readlines()))
    post_name = linecache.getline('post_name', line_number).strip()
    print('📢 < '+ post_name +' > ')
    case=random.randint(1, 5)
    print('📢 case : '+str(case))
    if case==1:
        driver.get('https://search.naver.com/search.naver?ie=UTF-8&query=%22'+post_name+'%22&sm=chr_hty')
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print('📢 [desktop] normal search complete')
        driver.find_element(By.CSS_SELECTOR, 'a[href*="blog.naver.com/stageinfo/"]').click()
        driver.switch_to.window(driver.window_handles[-1])
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    if case==2:
        driver.get('https://search.naver.com/search.naver?where=view&sm=tab_jum&query=%22'+post_name+'%22')
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print('📢 [desktop] view search complete')
        driver.find_element(By.CSS_SELECTOR, 'a[href*="blog.naver.com/stageinfo/"]').click()
        driver.switch_to.window(driver.window_handles[-1])
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    if case==3:
        driver.get('https://m.search.naver.com/search.naver?sm=mtp_hty.top&where=m&query=%22'+post_name+'%22')
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print('📢 [mobile] normal search complete')
        driver.find_element(By.CSS_SELECTOR, 'a[href*="m.blog.naver.com/stageinfo/"]').click()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    if case==5:
        driver.get('https://koreanfestivalguide.wordpress.com/2023/04/03/about-the-april-and-may-music-festival-in-korea/')
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print('📢 wordpress load complete')
        matching_links = []
        links = driver.find_elements(By.TAG_NAME, "a")
        matching_links = []
        for link in links:
            if link.get_attribute('href') is None:
                continue
            else:
                if 'https://blog.naver.com/stageinfo' in link.get_attribute('href'):
                    matching_links.append(link)
        if matching_links:
            random_link = random.choice(matching_links)
            print("📢 " +random_link.get_attribute('href')+' '+random_link.text)
            random_link.click()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    print('📢 post load complete')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('📢 scrooll down')
    wait=random.randint(40, 80)
    print('📢 wating : '+str(wait)+'sec')
    time.sleep(wait)
    driver.quit()

if __name__=="__main__":
    while True:
        ip = get_tor_ip()
        while ip in USED_IPS:
            ip = get_tor_ip()
            print("📢 IP already used, trying another one")
        USED_IPS.add(ip)
        print(f"📢 Current IP : {ip}")
        gmt_now = datetime.datetime.utcnow()
        kst_now = gmt_now + datetime.timedelta(hours=9)
        print(f"📢 Current TIME : {kst_now}")
        try:
            open_url()
            COUNT += 1
            print(f"📢 {COUNT} times complete")
            if COUNT > 1000 :
                COUNT = 0

        except:
            pass