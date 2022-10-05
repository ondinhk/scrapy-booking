import urllib.request
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from threading import Thread
from time import sleep, perf_counter
import logging

logging.basicConfig(filename="./log/std_page.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='w', )

# Let us Create an object
logger = logging.getLogger()
# Now we are going to Set the threshold of logger to DEBUG
logger.setLevel(logging.INFO)
# Waiting 20s for page load
DELAY = 20

CHROME = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def get_content_page(base_url, idx, category, chrome):
    chrome.get(base_url)
    html = chrome.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # query
    q_title = soup.find('h2', class_='d2fee87262 pp-header__title')
    q_description = soup.find('div', class_='hp_desc_main_content')
    q_cost_original = soup.find_all('div', class_='bui-price-display__original')
    q_cost_new = soup.find_all('div', class_='bui-price-display__value')
    q_number_comment = soup.find('span', class_='b5cd09854e c90c0a70d3 db63693c62')
    q_rate = soup.find('div', class_='b5cd09854e d10a6220b4')
    q_label = soup.find('span', class_='b5cd09854e f0d4d6a2f5 e46e88563a')
    # get text
    try:
        title = q_title.getText().strip('\t\r\n')
        description = q_description.getText().strip('\t\r\n').replace('Tôi muốn xem thêm', '')
        number_comment = q_number_comment.getText().strip('\t\r\n')
        rate = q_rate.getText().strip('\t\r\n')
        label_rate = q_label.getText().strip('\t\r\n')
        try:
            images = get_images(base_url)
        except Exception as e:
            logger.error("{} - {}".format(idx, 'Cannot get images'))
            return
        try:
            cost_original = q_cost_original[0].getText().strip('\t\r\n')
            cost_new = q_cost_new[0].getText().strip('\t\r\n')
        except:
            cost_original = q_cost_original.getText().strip('\t\r\n')
            cost_new = 0
        object = {'idHouse': idx,
                  'title': title,
                  'images': images,
                  'costOriginal': cost_original,
                  'costNew': cost_new,
                  'numberOfComment': number_comment,
                  'rate': rate,
                  'label': label_rate,
                  'category': category,
                  'description': description}
        logger.info("{} - {}".format(object, idx))
    except Exception as e:
        logger.info("{} - {}".format(idx, e))
        return

def get_images(url):
    return "anc"


def export_data_to_json(name, data):
    with open('./data/' + name + '.json', 'w') as f:
        json.dump(data, f)
    print("Export {} Done".format(name))
    logger.warning("LOCATIONS: {} number {}".format(name, len(data)))


def load_file_json(file_name):
    f = open('data/' + file_name)
    data = json.load(f)
    return data


def test():
    global CHROME
    a = load_file_json('da_lat.json')
    get_content_page(a[0], 0, category=1, chrome=CHROME)


if __name__ == '__main__':
    test()
