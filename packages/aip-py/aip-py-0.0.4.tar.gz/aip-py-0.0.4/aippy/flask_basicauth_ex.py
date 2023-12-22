#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-11-09 14:50
# @Author  : Jack
# @File    : flask_basicauth_ex.py
import base64
import logging
import time

import requests
from flask import current_app, request
from flask_basicauth import BasicAuth as basicAuth

"""
flask_basicauth_ex
"""
"""
flask_basicauth_ex
    实现aip平台业务
    1.授权验证
    2.记录访问日志
"""


__API_STATS_TAG__ = 'APISTATSTAG'


class BasicAuth(basicAuth):
    def __init__(self, app=None):
        self.aip_auth_refresh = 3600
        self._AUTH_CACHE = []
        super().__init__(app)

    def init_app(self, app):
        """
        Initialize this BasicAuth extension for the given application.

        :param app: a :class:`~flask.Flask` instance
        """
        app.config.setdefault('BASIC_AUTH_FORCE', False)
        app.config.setdefault('BASIC_AUTH_REALM', '')
        self.aip_auth_refresh = app.config.get('aip_auth_refresh', self.aip_auth_refresh)

        @app.before_request
        def require_basic_auth():
            logging.info(f"{__API_STATS_TAG__}\tbefore\t{request.path}")

            if not current_app.config['BASIC_AUTH_FORCE']:
                return
            if not self.authenticate():
                return self.challenge()

    def check_credentials(self, username, password):
        auth_str = base64.b64encode("{}:{}".format(username, password).encode('utf-8')).decode('utf-8')
        correct_auths = self.get_auths()
        username = correct_auths.get(auth_str)
        result = True if username and len(username) > 0 else False

        logging.info(f"{__API_STATS_TAG__}\tauth\t{request.path}\t{username}\t{result}")
        return result

    def get_auths(self):
        if len(self._AUTH_CACHE) == 0 or (time.time() - self._AUTH_CACHE[0]) > self.aip_auth_refresh:
            self._AUTH_CACHE = [time.time(), self.request_auths()]
            logging.info(f"{__API_STATS_TAG__}\trefreshauth\t{len(self._AUTH_CACHE[1])}")
        return self._AUTH_CACHE[1]

    def request_auths(self):
        """
        request_auths
        :return: {}
        """
        response = requests.session().post(current_app.config['aip_auth_url'],
                                           json={"appName": current_app.config['aip_appName']},
                                           headers={"token": current_app.config['aip_auth_token']})
        result = {}
        if response.status_code == 200:
            ret = response.json()
            if ret.get('success'):
                for i in ret.get("data"):
                    result.update({i['clientAuthorization']: i['clientName']})
        return result
