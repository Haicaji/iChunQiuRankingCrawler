from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

from Browser import Browser


def main():
    sysconfig = {
        "browser_location": "./ChromeWithDriver/chrome.exe",
        "driver_location": "./ChromeWithDriver/chromedriver112.exe",
        "headless": "False"
    }
    browser = Browser(system_config=sysconfig)
    browser.creat_browser()

    driver = browser.driver
    url = 'https://match.ichunqiu.com/situation/problems?k=AzZQYAEyBmZWPlVkB3YBIwEjAWRUd1QvUmsCNlRhCj1VYFFmCjoAZAs4AGEDNFw9'
    driver.get(url)

    element = driver.find_element(By.CSS_SELECTOR,
                                  "#app > div > div.container > div:nth-child(2) > div.el-pagination.is-background > span.el-pagination__total.is-first")
    all_num = int(element.text.replace("共 ", "").replace(" 条", ""))
    page_num = all_num // 10 + 1 if all_num % 10 != 0 else all_num // 10

    all_rank = []
    for now_page_num in range(page_num, 1, -1):
    # for now_page_num in range(3, 1, -1):
        input_page_num = driver.find_element(By.XPATH,
                                             '/html/body/div[1]/div/div[2]/div[2]/div[3]/span[2]/div/div/input')

        input_page_num.click()
        input_page_num.send_keys(Keys.CONTROL, 'a')
        input_page_num.send_keys(now_page_num)
        input_page_num.send_keys(Keys.RETURN)

        # 等待请求完成
        time.sleep(2)

    log_list = driver.get_log('performance')
    for log in log_list:
        log['message'] = json.loads(log['message'])['message']
        try:
            if log['message']['params']['response']['url'] == r'https://apiterminator.ichunqiu.com/match/rank/solved':
                # 传入request_id 获得响应的数据
                content = driver.execute_cdp_cmd('Network.getResponseBody',
                                                 {'requestId': log['message']['params']['requestId']})
                # 获取body对应的数据
                response_body = content['body']
                all_rank.append(response_body)
        except:
            pass

    all_rank = [json.loads(i)['data']['lists'] for i in all_rank]
    all_rank = [i for j in all_rank for i in j]

    # 把all_rank写入json文件
    with open('all_rank.json', 'w') as f:
        json.dump(all_rank, f)


if __name__ == '__main__':
    main()
