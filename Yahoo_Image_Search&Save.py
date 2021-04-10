import datetime
import os
from time import sleep
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import pandas as pd

chrome_path = r'C:\Users\dudvp_000\anaconda3\chromedriver'

options = Options()
options.add_argument('--incognito')

driver = webdriver.Chrome(executable_path=chrome_path, options=options)

url = 'https://search.yahoo.co.jp/image'
driver.get(url)

sleep(random.randint(1, 5))

query = input('検索ワードを入力＞')
search_box = driver.find_element_by_name('p')
search_box.clear()
search_box.send_keys(query)
search_box.submit()

sleep(1)

height = 1000
while height < 3000:
    driver.execute_script(f'window.scrollTo(0, {height});')
    height += 100
    print(height)
    sleep(1)

elements = driver.find_elements_by_class_name('sw-Thumbnail__image')

d_list = []
for i, element in enumerate(elements, start=1):
    name = f'{query}_{i}'
    # raw_url = element.find_element_by_class_name()
    google_image_url = element.find_element_by_tag_name('img').get_attribute('src')
    title = element.find_element_by_tag_name('img').get_attribute('alt')

    d = {
        'filename': name,
        # 'raw_url': raw_url,
        'google_image_url': google_image_url,
        'title': title
    }

    d_list.append(d)

df = pd.DataFrame(d_list)
df.to_csv(f'image_urls_{datetime.date.today()}.csv', index=None, encoding='utf-8-sig')

driver.quit()

IMAGE_DIR = './images/'

df = pd.read_csv(f'image_urls_{datetime.date.today()}.csv')

if os.path.isdir(IMAGE_DIR):
    print('すでにあります')
else:
    os.makedirs(IMAGE_DIR)

for file_name, google_image_url in zip(df.filename[:5], df.google_image_url[:5]):
    image = requests.get(google_image_url)
    with open(IMAGE_DIR + file_name + '.jpg', 'wb') as f:
        f.write(image.content)
