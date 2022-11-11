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
import random

# now we will Create and configure logger
logging.basicConfig(filename="./log/get_pages.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='w', )
# Let us Create an object
logger = logging.getLogger()
# Now we are going to Set the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

# Set GLOBAL VARIABLE
TIME_SLEEP_FROM = 3
TIME_SLEEP_TO = 7
AROUND = 1


def startThread():
    start_time = perf_counter()
    group_1 = load_file_json('group_1.json')
    group_2 = load_file_json('group_2.json')
    group_3 = load_file_json('group_3.json')
    group_4 = load_file_json('group_4.json')
    # Create Thread
    logger.info("Start thread")
    thread1 = Thread(target=run_process, args=(group_1, 'group1',))
    thread2 = Thread(target=run_process, args=(group_2, 'group2',))
    thread3 = Thread(target=run_process, args=(group_3, 'group3',))
    thread4 = Thread(target=run_process, args=(group_4, 'group4',))
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
        location = item['location']
        link = item['link']
        get_page(link=link, location=location, driver_chrome=driver_chrome, data=group_data)
    exportDataToJson(name=name, data=group_data)
    driver_chrome.quit()


def get_page(link, location, driver_chrome, data):
    driver_chrome.get(link)
    print_log_and_sleep(link)
    html = driver_chrome.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # Query find and get value
    try:
        # Get header__title
        try:
            query_header = soup.find('div', class_='header-name header-addr row')
            name_hotels = query_header.find('h1').get_text(strip=True)
            address = query_header.find('div', class_='margin-bottom-10 item-address').get_text(strip=True)
        except Exception as e:
            print_logger(link=link, message="Cannot get name and address", error=e)
        # Get description
        try:
            query_content = soup.find('div', class_='col-xs-12 col-sm-8')
            list_description = query_content.find_all('p')
            description = ''
            for item in list_description:
                description = description + ' ' + item.get_text(strip=True)
            description.replace('  Điểm nổi bật:  ', '')
        except Exception as e:
            print_logger(link=link, message="Cannot get description", error=e)
        # Get reviews
        try:
            reviews = random_rate()
        except Exception as e:
            print_logger(link=link, message="Cannot get reviews", error=e)
        # Locations around
        try:
            query_location_around = soup.find('div', {"id": "content_page_d_short"})
            list_location = query_location_around.find_all('li')
            location_around = []
            for item in list_location:
                name = item.find('div', class_='des-name').get_text(strip=True)
                distant = item.find('div', class_='des-distant').get_text(strip=True).replace(' km', '')
                obj_tmp = {name: float(distant)}
                location_around.append(obj_tmp)
        except Exception as e:
            print_logger(link=link, message="Cannot get Locations around", error=e)
        # Get images
        try:
            container_images = soup.find('div', class_='owl-stage-outer')
            list_images = container_images.find_all('img')
            images = []
            for item in list_images:
                if item.has_attr('src'):
                    images.append(item['src'])
        except Exception as e:
            print_logger(link=link, message="Cannot get images", error=e)
        # Get facility
        try:
            query_facility = soup.find('div', class_='facility')
            list_facility = query_facility.find_all('div', class_='item')
            facility = []
            for item in list_facility:
                facility.append(item.get_text(strip=True))
        except Exception as e:
            print_logger(link=link, message="Cannot get facility", error=e)
        # Get cost
        try:
            # Get 2 value
            cost_original = int(query_header.find('span', class_='price-origin price-origin-1395').get_text(
                strip=True).replace('đ', '').replace('.', ','))
            cost_sale = int(query_header.find('span', class_='text-price price-from price-from-1395').get_text(
                strip=True).replace('đ', '').replace('.', ','))
        except:
            try:
                # Get 1 value
                cost_sale = 'Chưa có khuyến mãi'
                cost_original = int(query_header.find('span', class_='text-price price-from price-from-1457').get_text(
                    strip=True).replace('đ', '').replace('.', ','))
            except:
                cost_sale = 'Chưa có khuyến mãi'
                cost_original = random_cost()
        obj = {'name': name_hotels,
               'location': location,
               'address': address,
               'cost_original': cost_original,
               'cost_sale': cost_sale,
               'reviews': reviews,
               'facility': facility,
               'location_around': location_around,
               'description': description,
               'images': images}
        data.append(obj)
    except Exception as e:
        print(e)


def random_cost():
    return round((random.randint(990000, 4990000)) / 10000) * 10000


def random_rate():
    rate = round(random.uniform(7.0, 9.7), 1)
    if rate <= 7.9:
        number_reviews = random.randint(44, 100)
    elif rate >= 8.9:
        number_reviews = random.randint(33, 111)
    else:
        number_reviews = random.randint(22, 412)
    return {'rate': rate, 'number_reviews': number_reviews}


def exportDataToJson(name, data):
    with open('./data/hotels/' + name + '.json', 'w') as f:
        json.dump(data, f)
    print("Export {} done -- {} Hotels".format(name, len(data)))
    logger.info("Export {} done -- {} Hotels".format(name, len(data)))


def print_log_and_sleep(link):
    time_sleep = round(random.randrange(TIME_SLEEP_FROM, TIME_SLEEP_TO, AROUND))
    logger.info("{} - Sleep: {}".format(link, time_sleep))
    print("{} - Sleep: {}".format(link, time_sleep))
    sleep(time_sleep)


def print_logger(link, message, error):
    logger.error("{} - {} - {}".format(link, message, error))
    print("{} - {} - {}".format(link, message, error))


def load_file_json(file_name):
    f = open('data/' + file_name)
    data = json.load(f)
    return data


def test():
    driver_chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    link_2_cost = 'https://bestprice.vn/khach-san/vinoasis-phu-quoc-1395.html'
    link_1_cost = 'https://www.bestprice.vn/khach-san/khach-san-delta-sapa-1457.html'
    link_0_cost = 'https://www.bestprice.vn/khach-san/altara-serviced-residences-quy-nhon-3426.html'
    test_link = 'https://www.bestprice.vn/khach-san/khach-san-hotel-colline-da-lat-1594.html'
    get_page(link=link_2_cost, location=1,
             driver_chrome=driver_chrome, data=[])


if __name__ == '__main__':
    # test()
    startThread()
