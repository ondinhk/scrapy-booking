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
DELAY = 2
DELAY_POPUP = 1

# Skip string
def start_thread():
    dalat = load_file_json('da_lat.json')
    danang = load_file_json('da_nang.json')
    nhatrang = load_file_json('nha_trang.json')
    phuquoc = load_file_json('phu_quoc.json')
    vungtau = load_file_json('vung_tau.json')
    start_time = perf_counter()
    # Create Thread
    logger.info("Start thread")
    thread1 = Thread(target=crawl, args=(dalat, 1, '1_dalat',))
    thread2 = Thread(target=crawl, args=(danang, 2, '2_danang',))
    thread3 = Thread(target=crawl, args=(nhatrang, 3, '3_nhatrang',))
    thread4 = Thread(target=crawl, args=(vungtau, 4, '4_vungtau',))
    thread5 = Thread(target=crawl, args=(phuquoc, 5, '5_phuquoc',))
    # Start Thread
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    # Wait to done
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    end_time = perf_counter()
    print(f'It took {end_time - start_time: 0.2f} second(s) to complete.')
    logger.info("End thread {}".format(end_time - start_time))


def crawl(data, category, name):
    temp = []
    chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    for idx, item in enumerate(data):
        try:
            temp.append(get_content_page(item, idx, category, chrome=chrome))
        except:
            continue
    export_data_to_json(name, temp)


def get_content_page(link, idx, idLocation, chrome):
    global DELAY
    chrome.get(link)
    sleep(DELAY)
    html = chrome.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # query
    q_title = soup.find('h2', class_='d2fee87262 pp-header__title')
    q_description = soup.find('div', class_='hp_desc_main_content')
    q_address = soup.find('span', class_='hp_address_subtitle js-hp_address_subtitle jq_tooltip')
    q_number_comment = soup.find('span', class_='b5cd09854e c90c0a70d3 db63693c62')
    q_rate = soup.find('div', class_='b5cd09854e d10a6220b4')
    q_label = soup.find('span', class_='b5cd09854e f0d4d6a2f5 e46e88563a')
    # get text
    try:
        title = q_title.get_text(strip=True)
        description = q_description.get_text(strip=True).replace('Tôi muốn xem thêm', '')
        address = q_address.get_text(strip=True)
        try:
            number_comment = q_number_comment.get_text(strip=True).replace('·','')
            rate = q_rate.get_text(strip=True)
            label_rate = q_label.get_text(strip=True)
        except:
            number_comment = "Chưa có đánh giá"
            rate = '0'
            label_rate = '0'
        try:
            q_cost_original = soup.find_all('div',
                                            class_='bui-f-color-destructive js-strikethrough-price prco-inline-block-maker-helper bui-price-display__original')
            q_cost_new = soup.find_all('div',
                                       class_='bui-price-display__value prco-text-nowrap-helper prco-inline-block-maker-helper prco-f-font-heading')
            cost_original = q_cost_original[0].get_text(strip=True).replace('\xa0',' ')
            cost_new = q_cost_new[0].get_text(strip=True).replace('\xa0',' ')
        except:
            try:
                q_cost_original = soup.find_all('div',
                                                class_='bui-price-display__value prco-text-nowrap-helper prco-inline-block-maker-helper prco-f-font-heading')
                cost_original = cost_original = q_cost_original[0].get_text(strip=True).replace('\xa0',' ')
                cost_new = 'Hiện chưa có khuyến mãi'
            except:
                cost_original = 'Update'
                cost_new = 'Update'
        try:
            images = get_images(chrome, link)
        except Exception as e:
            logger.error("{} - {} - {}".format(idx, 'Cannot get images', title))
            return
        logger.info("{} - {} - {}".format(idx, 'Done', title))
        object = {'idHouse': idx,
                  'idLocation': idLocation,
                  'name': title,
                  'address': address,
                  'costOriginal': cost_original,
                  'costNew': cost_new,
                  'numberOfComment': number_comment,
                  'rate': rate,
                  'label': label_rate,
                  'description': description,
                  'images': images}
        return object
    except Exception as e:
        logger.error("{} - {} - {}".format(idx, e, link))
        return

def get_images(chrome, link):
    global DELAY_POPUP
    try:
        # find button show all images
        sleep(DELAY_POPUP)
        open_pop_images = chrome.find_element(By.CLASS_NAME, 'bh-photo-grid-item.bh-photo-grid-thumb.js-bh-photo-grid-item-see-all')
        chrome.execute_script("arguments[0].click();", open_pop_images)
        sleep(DELAY_POPUP)
        try:
            object_images = []
            html = chrome.page_source
            soup = BeautifulSoup(html, 'html.parser')
            images = soup.find_all('img', class_='bh-photo-modal-grid-image')
            for item in images:
                if item.has_attr('src'):
                    object_images.append(item['src'])
            return object_images
        except Exception as e:
            logger.error("{} - {}".format("Cannot get images", link))
            return
    except Exception as e:
        logger.info("{} - {}".format(e, link))
        return
    return object_images


def export_data_to_json(name, data):
    with open('./data/' + name + '.json', 'w') as f:
        json.dump(data, f)
    print("Export {} Done".format(name))
    logger.warning("LOCATIONS: {} number {}".format(name, len(data)))


def load_file_json(file_name):
    f = open('data/' + file_name)
    data = json.load(f)
    return data

def test_image():
    url = 'https://www.booking.com/hotel/vn/vung-tau-gold-sea-apartment-cookies-homestay-can-ho-bien.vi.html?label=gen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEJuAEZyAEM2AED6AEBiAIBqAIDuAKn0ryZBsACAdICJDFjN2ZiNTNlLTkyYzYtNDdjOS05NTg3LTEyMGFmZjZlMjM0NtgCBOACAQ&sid=87b657754f8327f14759b75311b5a649&aid=304142&ucfs=1&arphpl=1&checkin=2022-10-10&checkout=2022-10-11&dest_id=-3733750&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=4&hapos=4&sr_order=popularity&srpvid=3c928a0463a00295&srepoch=1664048266&all_sr_blocks=905058201_361559050_3_42_0&highlighted_blocks=905058201_361559050_3_42_0&matching_block_id=905058201_361559050_3_42_0&sr_pri_blocks=905058201_361559050_3_42_0__64449000&from_beach_sr=1&beach_sr_walking_distance=923&tpi_r=2&from_sustainable_property_sr=1&from=searchresults#hotelTmpl'
    chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    chrome.get(url)
    images = get_images(chrome, link=url)
    print(images)

def test_file_json():
    a = load_file_json('5_phuquoc.json')
    b = load_file_json('4_vungtau.json')
    print(a)
    print(b)

def test_get_page():
    link = 'https://www.booking.com/hotel/vn/delen-house-thanh-pho-da-lat4.vi.html?aid=304142&label=gen173nr-1DCAMo9AE40wNIKlgEaPQBiAEBmAEquAEZyAEM2AED6AEB-AECiAIBqAIDuAKC_7yZBsACAdICJGE5MTMyZTJlLTVjYjEtNGQ2Yy04Y2RhLWZmYTJiZjcyZWIzYtgCBOACAQ&sid=87b657754f8327f14759b75311b5a649&all_sr_blocks=906463701_361730965_2_0_0;checkin=2022-10-10;checkout=2022-10-11;dest_id=-3712045;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=8;highlighted_blocks=906463701_361730965_2_0_0;hpos=8;matching_block_id=906463701_361730965_2_0_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=906463701_361730965_2_0_0__25000000;srepoch=1664048266;srpvid=55708a04d70d027f;type=total;ucfs=1&#hotelTmpl'
    idx = 0
    category = 1
    chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    print(get_content_page(link, idx, category, chrome))

if __name__ == '__main__':
    test_get_page()
    # test_image()
    # test_file_json()
    # start_thread()
