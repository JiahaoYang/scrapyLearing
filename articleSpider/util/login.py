import pickle
import time
import requests
from selenium import webdriver

# 半自动登录
# chrome_path = r'/Users/jiahaoyang/anaconda3/envs/learing/chromedriver'
# wd = webdriver.Chrome(executable_path=chrome_path)
# time.sleep(45)
# req = requests.Session()
# cookies = wd.get_cookies()
# for cookie in cookies:
#     req.cookies.set(cookie['name'], cookie['value'])
# req.headers.clear()
# response = req.get('https://www.zhihu.com')
# with open('index.html', 'wb') as f:
#     f.write(response.text.encode('utf8'))

# 登录微博
# chrome_path = r'/Users/jiahaoyang/anaconda3/envs/learing/chromedriver'
# wd = webdriver.Chrome(executable_path=chrome_path)
# wd.get('https://www.weibo.com/login.php')
#
# try:
#     wd.execute_script("document.getElementById('loginname').value='13806188295';")
# except:
#     pass
#
# try:
#     wd.execute_script("document.querySelector('#pl_login_form > div > div:nth-child(3) > "
#                       "div.info_list.password > div > input').value='mikasanvshen1,';")
# except:
#     pass
#
# try:
#     wd.execute_script("document.querySelector('#pl_login_form > div > div:nth-child(3) "
#                       "> div:nth-child(6) > a').click();")
# except:
#     pass
# code = str(input("input the code: "))
# script = "document.querySelector('#pl_login_form > div > div:nth-child(3) " \
#          "> div.info_list.verify.clearfix > div > input').value='" + code + "';"
#
# try:
#     wd.execute_script(script)
# except:
#     pass
#
# try:
#     wd.execute_script("document.querySelector('#pl_login_form > div "
#                       "> div:nth-child(3) > div:nth-child(6) > a').click();")
# except:
#     pass
#
# req = requests.Session()
# cookies = wd.get_cookies()
# for cookie in cookies:
#     req.cookies.set(cookie['name'], cookie['value'])
# test = req.get('https://www.weibo.com')


# 第三方登录知乎
wd = webdriver.Chrome(executable_path=r'/Users/jiahaoyang/anaconda3/envs/learing/chromedriver')
wd.get('https://www.zhihu.com/signup?next=%2F')
wd.find_element_by_xpath(
    '//*[@id="root"]/div/main/div/div/div/div[2]/div[2]/span').click()
wd.find_element_by_xpath(
    '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[5]/span[5]/button').click()
wd.find_element_by_xpath(
    '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[5]/span[5]/span/button[2]').click()
try:
    wd.execute_script("document.getElementById('userId').value='13806188295';")
except:
    pass
try:
    wd.execute_script("document.getElementById('passwd').value='mikasanvshen1,';")
except:
    pass
wd.find_element_by_xpath('//*[@id="outer"]/div/div[2]/form/div/div[2]/div/p/a[1]').click()
time.sleep(1)
wd.find_element_by_xpath('//a[@node-type="submit"]').click()
cookies = wd.get_cookies()
pickle.dump(cookies, open('cookie.pkl', 'wb'))
req = requests.Session()
for cookie in cookies:
    req.cookies.set(cookie['name'], cookie['value'])
req.headers.clear()
test = req.get('https://www.zhihu.com')


# 加载本地cookie
# wd = webdriver.Chrome(executable_path=r'/Users/jiahaoyang/anaconda3/envs/learing/chromedriver')
# cookies = pickle.load(open('cookie.pkl', 'rb'))
# req = requests.Session()
# for cookie in cookies:
#     req.cookies.set(cookie['name'], cookie['value'])
# req.headers.clear()
# test = req.get('https://www.zhihu.com')
# print(test)




