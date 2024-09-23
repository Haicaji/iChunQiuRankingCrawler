# 生成UA
from fake_useragent import UserAgent


class UaCreate:
    def __init__(self):
        pass

    def get_ua(self, is_mobile=False):
        user_agent = UserAgent()
        ua = user_agent.random
        if not is_mobile:
            while 'Mobile' in ua or 'Android' in ua or 'iPhone' in ua:
                ua = user_agent.random

        return ua