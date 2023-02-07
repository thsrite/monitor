import logging
import yaml
import os
import requests
import time
import wechat

logging.basicConfig(filename="monitor", format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S ',
                    level=logging.INFO)
logger = logging.getLogger()
KZT = logging.StreamHandler()
KZT.setLevel(logging.DEBUG)
logger.addHandler(KZT)

if __name__ == '__main__':
    filepath = os.path.join("/mnt/",
                            'config.yaml')  # 文件路径,这里需要将a.yaml文件与本程序文件放在同级目录下
    with open(filepath, 'r') as f:  # 用with读取文件更好
        configs = yaml.load(f, Loader=yaml.FullLoader)  # 按字典格式读取并返回

    if bool(configs["monitor"]["status"]) == True:
        while True:

            for url in configs["monitor"]["urls"]:
                req = requests.get(url=url['url'])

                if int(req.status_code) == 200:
                    res = req.content
                    if str(url['keyword']) not in str(res):
                        senWx = wechat.SendWeiXinWork()
                        senWx.send_message(url['name'] + "到货了\n" + url['url'])
                        logger.info(url['name'] + "到货了\n" + url['url'])
                    else:
                        if bool(configs["monitor"]["log"]) == True:
                            logger.warning(url['name'] + " 缺货，持续刷新中（" + url['keyword'] + "）")

                time.sleep(int(configs["monitor"]["time"]))
