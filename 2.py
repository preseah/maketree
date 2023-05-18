import random
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from requests import get
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
import datetime
USED_IPS = set()
MAX_IPS = 1000

url   = 'https://koreanfestivalguide.wordpress.com/2023/04/03/about-the-april-and-may-music-festival-in-korea/'

def get_tor_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="1234qwer")
        controller.signal(Signal.NEWNYM)
        time.sleep(controller.get_newnym_wait())
        # options = webdriver.ChromeOptions()
        # options.add_argument('--proxy-server=%s' % hostname + ":" + port) 
        # user_agent = UserAgent().random
        # options.add_argument(f'user-agent={user_agent}')
        # options.add_argument('headless')
        # driver = webdriver.Chrome('/usr/lib64/chromium-browser/chromedriver', chrome_options=options)
        # driver.get('https://ident.me')
        # ip = driver.find_element(By.XPATH, "/html/body/pre").text
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
    print('move to wordpress')
    driver.get(url)
    driver.implicitly_wait(5)
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
    driver.implicitly_wait(5)
    print('📢 naver load complete')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait=random.randint(60, 120)
    print('📢 wating : '+str(wait)+'sec')
    time.sleep(wait)
    driver.quit()

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
            open_url(url)
        except:
            pass
        end=random.randint(10,70)
        print(end)
        time.sleep(end)




