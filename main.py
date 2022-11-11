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
logging.basicConfig(filename="./log/std.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='w', )
# Let us Create an object
logger = logging.getLogger()
# Now we are going to Set the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

DELAY = 20


def startThread():
    # 808
    da_lat = 'https://www.booking.com/searchresults.vi.html?aid=304142&label=gen173nr-1DCAMo9AE40wNIKlgEaPQBiAEBmAEquAEZyAEM2AED6AEB-AECiAIBqAIDuAKC_7yZBsACAdICJGE5MTMyZTJlLTVjYjEtNGQ2Yy04Y2RhLWZmYTJiZjcyZWIzYtgCBOACAQ&sid=5d02569ba80a5b28736693dfc5d32e0c&checkin=2022-12-01&checkout=2022-12-02&city=-3712045&'
    # 947
    da_nang = 'https://www.booking.com/searchresults.vi.html?aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEJuAEZyAEM2AED6AEBiAIBqAIDuAKn0ryZBsACAdICJDFjN2ZiNTNlLTkyYzYtNDdjOS05NTg3LTEyMGFmZjZlMjM0NtgCBOACAQ&sid=87b657754f8327f14759b75311b5a649&checkin_monthday=10&checkin_year_month=2022-10&checkout_monthday=11&checkout_year_month=2022-10&dest_id=-3712125&dest_type=city&from_history=1&group_adults=2&group_children=0&no_rooms=1&sb_travel_purpose=leisure&si=ad&si=ai&si=ci&si=co&si=di&si=la&si=re&srpvid=2f7e7afaf46200d1&&sh_position=3'
    # 585
    nha_trang = 'https://www.booking.com/searchresults.vi.html?aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEJuAEZyAEM2AED6AEBiAIBqAIDuAKn0ryZBsACAdICJDFjN2ZiNTNlLTkyYzYtNDdjOS05NTg3LTEyMGFmZjZlMjM0NtgCBOACAQ&sid=87b657754f8327f14759b75311b5a649&checkin=2022-10-10&checkout=2022-10-11&dest_id=-3723998&dest_type=city&srpvid=2f7e7afaf46200d1&'
    # 952
    vung_tau = 'https://www.booking.com/searchresults.vi.html?aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEJuAEZyAEM2AED6AEBiAIBqAIDuAKn0ryZBsACAdICJDFjN2ZiNTNlLTkyYzYtNDdjOS05NTg3LTEyMGFmZjZlMjM0NtgCBOACAQ&sid=87b657754f8327f14759b75311b5a649&checkin=2022-10-10&checkout=2022-10-11&dest_id=-3733750&dest_type=city&srpvid=2f7e7afaf46200d1&'
    # 439
    phu_quoc = 'https://www.booking.com/searchresults.vi.html?aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEJuAEZyAEM2AED6AEBiAIBqAIDuAKn0ryZBsACAdICJDFjN2ZiNTNlLTkyYzYtNDdjOS05NTg3LTEyMGFmZjZlMjM0NtgCBOACAQ&sid=87b657754f8327f14759b75311b5a649&checkin=2022-10-10&checkout=2022-10-11&dest_id=-3726177&dest_type=city&srpvid=2f7e7afaf46200d1&'
    # 631
    hoi_an = 'https://www.booking.com/searchresults.vi.html?aid=397594&label=gog235jc-1FCAEoggI46AdIM1gDaPQBiAEBmAEquAEZyAEM2AEB6AEB-AENiAIBqAIDuALY5qSbBsACAdICJDMyY2U1MDAxLWIwMjEtNDYxYy05NzUxLTZiZTcwNWIwZThjNtgCBuACAQ&sid=5d02569ba80a5b28736693dfc5d32e0c&checkin=2022-12-01&checkout=2022-12-02&city=-3715584&'

    start_time = perf_counter()
    # Create Thread
    logger.info("Start thread")
    thread1 = Thread(target=getAllLink, args=(da_lat, "da_lat_link",))
    thread2 = Thread(target=getAllLink, args=(da_nang, "da_nang_link",))
    thread3 = Thread(target=getAllLink, args=(nha_trang, "nha_trang_link",))
    thread4 = Thread(target=getAllLink, args=(vung_tau, "vung_tau_link",))
    thread5 = Thread(target=getAllLink, args=(phu_quoc, "phu_quoc_link",))
    thread6 = Thread(target=getAllLink, args=(hoi_an, "hoi_an_link",))
    # Start Thread
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    # Wait to done
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    end_time = perf_counter()
    print(f'It took {end_time - start_time: 0.2f} second(s) to complete.')
    logger.info("End thread")


def getAllLink(base_url, name):
    output = []
    idx = 0
    driver_chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    numberPage = getNumberPage(base_url, driver_chrome)
    print(numberPage)
    for i in range(numberPage):
        html = driver_chrome.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # list card
        container = soup.find_all('div',
                                  class_='a826ba81c4 fe821aea6c fa2f36ad22 afd256fc79 d08f526e0d ed11e24d01 ef9845d4b3 da89aeb942')
        for idex, item in enumerate(container):
            try:
                link = item.find('a', class_='e13098a59f')['href']
                output.append(link)
                idx += 1
            except Exception as e:
                logger.error(e)
                print(e)
                continue
        try:
            btn_next_page = driver_chrome.find_element(By.CSS_SELECTOR,
                                                       '#search_results_table > div:nth-child(2) > div > div > div > div.d7a0553560 > div.b727170def > nav > div > div.f32a99c8d1.f78c3700d2 > button')
            driver_chrome.execute_script("arguments[0].click();", btn_next_page)
            time_sleep = round(random.randrange(5, 10, 2))
            sleep(time_sleep)
        except Exception as e:
            logger.error(e)
            exportDataToJson(name, output)
            return
        logger.info("{} - {} - Sleep: {}".format(name, idx, time_sleep))
    exportDataToJson(name, output)
    driver_chrome.quit()


def getNumberPage(base_url, driver_chrome):
    driver_chrome.get(base_url)
    WebDriverWait(driver_chrome, DELAY)
    html = driver_chrome.page_source
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('li', class_='f32a99c8d1')
    number_page = int(pages[len(pages) - 1].getText())
    return number_page


def exportDataToJson(name, data):
    with open('./data/' + name + '.json', 'w') as f:
        json.dump(data, f)
    print("Export {} Done".format(name))
    logger.warning("LOCATIONS: {} number {}".format(name, len(data)))


if __name__ == '__main__':
    startThread()
