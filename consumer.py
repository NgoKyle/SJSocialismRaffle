import requests
import sys
import datetime
import time
import re
import random
import string
import threading
import json


from random import randint
from faker import Faker
fake = Faker('en_US')

class Consumer(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        for key, val in kwargs.items():
            setattr(self, key, val)


    def phone_gen(self,size=6, chars= string.digits):
        end = ''.join(random.choice(chars) for _ in range(size))
        number = '503' + end
        return number


    def enter(self, answer):
        print("Consumer Thread is Submitting Raffle...")

        name = fake.name().split(' ')
        getheaders = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0', 'if-modified-since': 'Fri, 05 Jan 2018 11',
            'if-none-match': '"42f-562062e8ef580-gzip"', 'upgrade-insecure-requests': '1',
            'user-agent': fake.user_agent()}

        s = requests.Session()
        j = s.get(self.url, headers=getheaders)

        sizes = ['36', '37 ½', '38 ½', '40', '41', '42 ½', '44', '45', '46']
        size = (random.choice(sizes))

        raw_date = datetime.datetime.now()
        r_date = str(raw_date).split(' ')[0]
        r_time = str(raw_date).split(' ')[1].split('.')[0]
        date_time = '{}T{}+00:00'.format(r_date, r_time)

        longnum = randint(10000, 1000000)
        email = self.prefix + str(longnum) + '@' + self.domain

        data = {"firstName":name[0],
                "lastName":name[1],
                "email":email,
                "phone":self.phone_gen(),
                "country":'840',
                "city":fake.address().split('\n')[1].split(',')[0],
                "order":[{"product":self.productNo,"size":size}],
                "raffle":self.raffleNo,
                "captcha":answer,
                "date":date_time
                }
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

        try:
            response = json.loads(g.text)

            if response['data'] == None and 'Order Already Placed' in str(g.text):
                print('Failed to enter, email combination already used, use a different email.'%x)
            elif response['data'] == None:
                print('Unexpected response from the server' % x)
            elif response['data']['requestOrder'] == True:
                print(name[0], name[1], email, size)
                data_string = '{} {}:{}:{}'.format(name[0], name[1], email, size)


                self.condition.acquire()
                logfile = open('logfile.txt', 'a')
                logfile.write(data_string + '\n')
                logfile.close()
                self.condition.release()
            else:
                print('Unexpected response from the server')


        except:
            continue
            # print("Unexpected error:", sys.exc_info()[0])

    def run(self):
        while True:
            time.sleep(2)
            if self.captchaList:
                self.condition.acquire()
                cap_answer=""

                try:
                    cap_answer = self.captchaList.pop(0)
                    self.condition.release()
                except:
                    self.condition.release()
                    continue
                self.enter(cap_answer)
