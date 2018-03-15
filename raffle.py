import threading
import sys
import time
from producer import Producer
from consumer import Consumer

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

def main():
    config = {}
    with open('./config.txt', 'r') as file:
        for line in file:
            line = line.rstrip()
            key, val = line.split('=')
            config[key] = val;
    file.close()

    captchaList = []
    condition = threading.Condition()

    producer = Producer(sitekey=config['sitekey'],
                       twocaptchaKey=config['twocaptchaKey'],
                       condition=condition,
                       producerNo=int(config['producerThread']),
                       captchaList=captchaList)
    producer.start()

    for i in range(int(config['consumerThread'])):
        consumer = Consumer(url=config['url'],
                            productNo=config['productNo'],
                            raffleNo=config['raffleNo'],
                            areCode=config['phoneAreaCode'],
                            domain =config['catchAllDomain'],
                            prefix=config['catchAllPrefix'],
                            condition=condition,
                            captchaList=captchaList)
        consumer.start()


if __name__=='__main__':
    main()
