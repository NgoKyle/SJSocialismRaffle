import requests
import datetime
import time
import re
import random
import string


from random import randint
from faker import Faker
fake = Faker()


def main():
    url='https://slamjamsocialism-drops.com/drops/53/'
    #enter(url)
    longnum = randint(10000, 1000000)
    email = 'cuong'+ str(longnum) + '@' + 'litcart1.club'
    print(email)

def phone_gen(size=6, chars= string.digits):
    end = ''.join(random.choice(chars) for _ in range(size))
    number = '503' + end
    return number

def twocaptcha():
    params = {'key':'44dbdbd8c7e51f8e0413ba5f5f5124be',
              'method':'userrecaptcha',
              'googlekey':'6LfYhz0UAAAAAJFKp28Sg0NnAEIPMfKI1RJSGsdB',
              'pageurl':'www.slamjamsocialism-drops.com'}
    r = requests.get("http://2captcha.com/in.php", params=params)
    while True:
        captcha_id = re.search(r'(?P<id>\d+)', r.text).group("id")
        r2=requests.get("http://2captcha.com/res.php?key=44dbdbd8c7e51f8e0413ba5f5f5124be&action=get&id=%s"
                      % captcha_id)
        if r2.text == "ERROR_CAPTCHA_UNSOLVABLE":
            print('invalid captcha...')
            break
        elif r2.text == "CAPCHA_NOT_READY":
            print(r2.text)
            time.sleep(5)
        else:
            answer = re.search(r'OK\|(?P<captcha_answer>.*)',r2.text).group("captcha_answer")
            print(answer)
            return answer

def enter(url):
    name = fake.name().split(' ')
    getheaders = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0', 'if-modified-since': 'Fri, 05 Jan 2018 11',
        'if-none-match': '"42f-562062e8ef580-gzip"', 'upgrade-insecure-requests': '1',
        'user-agent': fake.user_agent()}

    s = requests.Session()
    j = s.get(url, headers=getheaders)

    """
    phone = phone_gen()

    fake = Faker('en_US')
    """



    size_1 = str(randint(7,13))
    bool = randint(0,1)
    if bool == 0:
        size = str(size_1)
    else:
        size= str(size_1) + ' ½'

    raw_date = datetime.datetime.now()
    r_date = str(raw_date).split(' ')[0]
    r_time = str(raw_date).split(' ')[1].split('.')[0]
    date_time = '{}T{}+00:00'.format(r_date, r_time)

    #answer = twocaptcha()

    data = {"firstName":name[0],
            "lastName":name[1],
            "email":'dskjhfsdhjfhdkj@gmail.com',
            "phone":phone_gen(),
            "country":'840',
            "city":fake.address().split('\n')[1].split(',')[0],
            "order":[{"product":'48',"size":size}],
            "raffle":'53',
            #"captcha":answer,
            "date":date_time
            }
    for k,v in data.items():
        print(k,v)

    """
    headers = {'accept': '*/*',
               'accept-language': 'en-US,en;q=0.9',
               'authorization': 'null',
               'content-type': 'application/json',
               'origin': 'https', 'referer': 'https',
               'user-agent': fake.user_agent()
               }

    payload = {"query":"mutation RequestOrdertMutation($data: OrderRequestInput!) {\n  requestOrder(data: $data)\n}\n","operationName":"RequestOrdertMutation","variables":{"data":data}}


    g = s.post('https://slamjamsocialism-drops.com/graphql', headers=headers, json=payload, timeout=60)
    print(g.text)
    """

if __name__=='__main__':
    main()
