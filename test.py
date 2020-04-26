# import requests
import time

# meipian_url_html = 'https://m.meisheapp.com/person/index.html?id=2810203'
# meipian_url_user_detail = 'https://api.meisheapp.com/v1/user/detail?query_user_id=2810203&token=&user_id='
# meipian_url_video_list = 'https://community.meisheapp.com/meishe/user/?queryUserId=2810203&command=getUserFilmList&token=&userId=&maxNum=10&startId=21718803'

# response = requests.get(meipian_url_html)
# # print(strhtml.text)

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
#     'Connection': 'keep-alive',
#     'Pragma': 'no-cache',
#     'Cache-Control': 'no-cache',
#     'Accept': '*/*',
#     'Sec-Fetch-Dest': 'empty',
#     'Origin': 'https://m.meisheapp.com',
#     'Sec-Fetch-Site': 'same-site',
#     'Sec-Fetch-Mode': 'cors',
#     'Referer': 'https://m.meisheapp.com/person/index.html?id=2810203',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
# }


# response = requests.get(meipian_url_user_detail, headers=headers)
# res_data = response.json()
# print(res_data)

# from selenium import webdriver  # 导入库
# driver = webdriver.Chrome(executable_path='/Users/lixn/.bin/chromedriver')  # 声明浏览器
# url = 'https:www.baidu.com'
# driver.get(url)  # 打开浏览器预设网址
# time.sleep(5)     # Let the user actually see something!
# search_box = driver.find_element_by_id('kw')
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5)
# # print(driver.page_source)  # 打印网页源代码
# driver.close()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# service = Service('/Users/lixn/.bin/chromedriver')
# service.start()
driver = webdriver.Remote('http://127.0.0.1:9515')
driver.get('http://www.baidu.com/')
time.sleep(5)  # Let the user actually see something!
driver.quit()
