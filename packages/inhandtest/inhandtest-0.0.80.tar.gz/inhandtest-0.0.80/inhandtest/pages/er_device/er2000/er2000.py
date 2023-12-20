# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/9/19 15:00
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : EAP600.py
@IDE     : PyCharm
------------------------------------
"""

from playwright.sync_api import Page
from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.er_device.er2000.local_network import LocalNetwork
from inhandtest.pages.er_device.er2000.security import Security
from inhandtest.pages.er_device.er2000.vpn import Vpn
from inhandtest.pages.er_device.functions.functions import Internet
from inhandtest.telnet import Telnet
import dynaconf
import os


class ER2000(BasePage):

    def __init__(self, host: str, super_user: str, super_password: str, page: Page = None, model='ER2000',
                 language='en', protocol='https', port=443, username='adm', password='123456', **kwargs):
        """

        :param host:   设备主机地址
        :param super_user:  超级用户
        :param super_password: 超级用户密码
        :param page:  playwright page
        :param model:  设备型号  IG902 IG502
        :param language: 语言 en cn
        :param protocol: 协议  http https
        :param port:    端口
        :param username: 用户名
        :param password: 密码
        :param kwargs:
            telnet: 是否开启telnet, 默认为True 开启
            locale_yaml_path: 本地国际化文件路径
            bring_to_front: 是否将浏览器窗口置顶  默认为False 不置顶
            viewport: {'width': 1366, 'height': 768}  窗口大小
            web_login_timeout: int  登录超时时间 默认300， 单位秒 即5分钟， 监测到登录超时后，会自动重新登录
            version: 固件版本
        """
        telnet = kwargs.get('telnet', True)
        locale_yaml_path = kwargs.get('locale_yaml_path', None)
        bring_to_front = kwargs.get('bring_to_front', False)
        web_login_timeout = kwargs.get('web_login_timeout', 300)
        viewport = kwargs.get('viewport', {'width': 1366, 'height': 768})
        if locale_yaml_path:
            in_setting = dynaconf.Dynaconf(
                settings_files=[os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locale.yml'), locale_yaml_path],
                merge_enabled=True)
        else:
            in_setting = dynaconf.Dynaconf(
                settings_files=[os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locale.yml')])
        super().__init__(host, username, password, protocol, port, model, language, page, locale=in_setting,
                         bring_to_front=bring_to_front, viewport=viewport, web_login_timeout=web_login_timeout)
        if telnet:
            self.telnet = Telnet(model, host, super_user, super_password)
        else:
            self.telnet = None
        if self.language == 'en':
            self.telnet.send_cli(command='language English', type_='user')
        else:
            self.telnet.send_cli(command='language Chinese', type_='user')
        self.login()
        self.page.on("response", self.call_web_login_timeout)
        self.security = Security(host, username, password, protocol, port, model, language, self.page,
                                 locale=in_setting)
        self.internet = Internet(host, username, password, protocol, port, model, language, self.page,
                                 locale=in_setting)
        self.local_network = LocalNetwork(host, username, password, protocol, port, model, language, self.page,
                                          locale=in_setting)
        self.vpn = Vpn(host, username, password, protocol, port, model, language, self.page, locale=in_setting)

if __name__ == '__main__':
    from inhandtest.log import enable_log
    import re

    enable_log(console_level='debug')
    with ER2000('10.5.33.50', ) as device:
        device.config.lan.config()
        device.page.wait_for_timeout(10 * 1000)
