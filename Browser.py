import os
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service

from UA import UaCreate


# 浏然器对象
class Browser:
    def __init__(self, system_config):
        self.system_config = system_config
        self.options = None
        self.service = None
        self.driver = None

        self.set_driver()

    def set_driver(self):
        self.__set_options()
        self.__set_service()

    # 配置浏览器
    def __set_options(self):
        # 设置options
        self.options = webdriver.ChromeOptions()

        # 启用性能日志
        self.options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        # 设置chrome浏览器路径
        self.options.binary_location = self.system_config['browser_location']

        if self.system_config['headless'] == "True":
            # 设置无头浏览器
            self.options.add_argument('--headless')
            self.options.add_argument('--disable-gpu')

        # 忽略浏览器控制警告
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # 防止检测自动化
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_argument('--disable-blink-features=AutomationControlled')

        # 关闭浏然器自动关闭
        # self.options.add_experimental_option("detach", True)

        # 设置UA
        self.options.add_argument('user-agent=' + UaCreate().get_ua())

    def __set_service(self):
        # 设置chromedriver路径
        self.service = Service(os.path.abspath(self.system_config['driver_location']))

    def creat_browser(self):
        # 创建浏览器
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        # 设置最长刷新等待时间
        self.driver.implicitly_wait(10)
