import json
import logging
import random
from threading import Thread
from time import sleep, perf_counter

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# now we will Create and configure logger
logging.basicConfig(filename="log/get_all_links.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='w', )
# Let us Create an object
logger = logging.getLogger()
# Now we are going to Set the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

# Set GLOBAL VARIABLE
TIME_SLEEP_FROM = 3
TIME_SLEEP_TO = 5
AROUND = 1

# Data
BASE_URL = 'https://www.bestprice.vn'
group_1 = [
    {
        'name': 'quy_nhon',
        'link': 'https://www.bestprice.vn/khach-san/quy-nhon',
        'page': 7
    },
    {
        'name': 'nha_trang',
        'link': 'https://www.bestprice.vn/khach-san/nha-trang',
        'page': 16
    },
    {
        'name': 'ho_chi_minh',
        'link': 'https://www.bestprice.vn/khach-san/ho-chi-minh',
        'page': 20
    },
]
group_2 = [
    {
        'name': 'sapa',
        'link': 'https://www.bestprice.vn/khach-san/sapa',
        'page': 9
    },
    {
        'name': 'phu_quoc',
        'link': 'https://www.bestprice.vn/khach-san/phu-quoc',
        'page': 14
    },
    {
        'name': 'ha_long',
        'link': 'https://www.bestprice.vn/khach-san/ha-long',
        'page': 9
    },
]
group_3 = [
    {
        'name': 'da_lat',
        'link': 'https://www.bestprice.vn/khach-san/da-lat',
        'page': 10
    },
    {
        'name': 'da_nang',
        'link': 'https://www.bestprice.vn/khach-san/da-nang',
        'page': 21
    }
]
group_4 = [
    {
        'name': 'ha_noi',
        'link': 'https://www.bestprice.vn/khach-san/ha-noi',
        'page': 28
    },
    {
        'name': 'vung_tau',
        'link': 'https://www.bestprice.vn/khach-san/vung-tau',
        'page': 8
    }
]


def startThread():
    start_time = perf_counter()
    # Create Thread
    logger.info("Start thread")
    thread1 = Thread(target=run_process, args=(group_1, 'Group1',))
    thread2 = Thread(target=run_process, args=(group_2, 'Group2',))
    thread3 = Thread(target=run_process, args=(group_3, 'Group3',))
    thread4 = Thread(target=run_process, args=(group_4, 'Group4',))
    # Start Thread
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    # Wait to done
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    end_time = perf_counter()
    print(f'It took {end_time - start_time: 0.2f} second(s) to complete.')
    logger.info("End thread")


def run_process(groups, name):
    driver_chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    group_data = []
    for item in groups:
        name = item['name']
        link = item['link']
        number_page = item['page']
        data_tmp = get_all_link(name=name, link=link, number_page=number_page,
                                driver_chrome=driver_chrome, data = group_data)
    exportDataToJson(name=name, data=group_data)
    driver_chrome.quit()


def get_all_link(name, link, number_page, driver_chrome, data):
    idx = 0
    link_page = link
    for i in range(number_page):
        print_log_and_sleep(name=name)
        # Parser source
        link_page = link + '?page=' + str(i + 1)
        print(link_page)
        driver_chrome.get(link_page)
        html = driver_chrome.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # List items
        container = soup.find_all('li', class_='bpv-list-item hotel-ids')
        for item in container:
            try:
                sub_path = item.find('a', class_='margin-right-5')['href']
                base_link = BASE_URL + sub_path
                obj = {'location': name, 'link': base_link}
                data.append(obj)
                idx += 1
            except Exception as e:
                print_log_error(e)
                continue
        driver_chrome.get(link_page)


def exportDataToJson(name, data):
    with open('./data/' + name + '.json', 'w') as f:
        json.dump(data, f)
    print("Export {} done -- {} Hotels".format(name, len(data)))
    logger.info("Export {} done -- {} Hotels".format(name, len(data)))


def print_log_and_sleep(name):
    time_sleep = round(random.randrange(TIME_SLEEP_FROM, TIME_SLEEP_TO, AROUND))
    logger.info("{} - Sleep: {}".format(name, time_sleep))
    sleep(time_sleep)


def test():
    run_process(groups=group_1)


if __name__ == '__main__':
    startThread()
    # test()
