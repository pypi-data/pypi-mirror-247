"""
爬虫基类： ：pip install pytest-playwright -i https://pypi.tuna.tsinghua.edu.cn/simple/ -U
"""
import os
from typing import Callable

from afeng_tools.playwright_tool import http_header_tools, http_cookie_tools
from playwright.sync_api import Page

from afeng_tools.os_tool import os_tools


class BaseSpider:

    def __init__(self, spider_name: str, auth_save_path: str = None,
                 auth_cookie_file_name: str = '.auth_cookie.bin',
                 auth_header_file_name: str = '.auth_header.bin'):
        if auth_save_path is None:
            auth_save_path = os.path.join(os_tools.get_user_home(), f'.{spider_name}')
        os.makedirs(auth_save_path, exist_ok=True)
        self.cookie_file = os.path.join(auth_save_path, auth_cookie_file_name)
        self.header_file = os.path.join(auth_save_path, auth_header_file_name)

    def _refresh_auth(self, web_page: Page, auth_callback: Callable[[Page], None]):
        """刷新认证"""
        print('开始执行认证逻辑')
        http_header_tools.save_headers(web_page, self.header_file)
        auth_callback(web_page)
        print('结束执行认证逻辑')
        print('[保存]认证header')
        http_header_tools.save_headers(web_page, self.header_file)
        print('[保存]认证cookie')
        http_cookie_tools.save_cookies(web_page, self.cookie_file)

    def _load_auth_file(self, web_page: Page, auth_callback: Callable[[Page], None]):
        """加载认证文件"""
        if not os.path.exists(self.cookie_file) or not os.path.exists(self.header_file):
            self._refresh_auth(web_page=web_page, auth_callback=auth_callback)
        return self.header_file, self.cookie_file

    def load_auth(self, web_page: Page, auth_callback: Callable[[Page], None]):
        """
        加载认证
        :param web_page: Page
        :param auth_callback: 认证回调函数，内部实现认证逻辑
        :return:
        """
        print('加载认证信息')
        tmp_header_file, tmp_cookie_file = self._load_auth_file(web_page, auth_callback=auth_callback)
        http_header_tools.set_headers(page=web_page, auth_header_file=tmp_header_file)
        http_cookie_tools.set_cookies(page=web_page, auth_cookie_file=tmp_cookie_file)
