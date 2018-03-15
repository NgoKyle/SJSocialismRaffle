import requests
import re
import threading
import time

class Producer(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        for key, val in kwargs.items():
            setattr(self, key, val)

    def twocaptcha(self,i):
        print("Producer",i,"is harvesting captcha")
        while True:
            try:
                params = {'key':self.twocaptchaKey,
                          'method':'userrecaptcha',
                          'googlekey':self.sitekey,
                          'pageurl':'www.slamjamsocialism-drops.com'}
                r = requests.get("http://2captcha.com/in.php", params=params)

                while True:
                    captcha_id = re.search(r'(?P<id>\d+)', r.text).group("id")
                    r2=requests.get("http://2captcha.com/res.php?key=%s&action=get&id=%s"
                                    % (self.twocaptchaKey,captcha_id))
                    if r2.text == "ERROR_CAPTCHA_UNSOLVABLE":
                        print('invalid captcha...')
                        break
                    elif r2.text == "CAPCHA_NOT_READY":
                        time.sleep(5)
                    else:
                        answer = re.search(r'OK\|(?P<captcha_answer>.*)',r2.text).group("captcha_answer")
                        self.captchaList.append(answer)
                        print("Number of captcha tokens harvested:",len(self.captchaList))
                        break
            except:
                continue

    def run(self):
        for i in range(self.producerNo):
            t = threading.Thread(target=self.twocaptcha, args=(i,))
            t.start()
