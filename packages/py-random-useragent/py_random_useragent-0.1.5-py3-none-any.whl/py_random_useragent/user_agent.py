# -*- coding: utf-8 -*-
# @Author: Suvorinov Oleg <olegsuvorinov@me.com>
# @Date:   2023-02-28 10:01:30
# @Last Modified by:   Suvorinov Oleg
# @Last Modified time: 2023-12-21 19:33:15

import random

import requests

U_A = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0' # noqa


class UserAgent(object):
    """docstring for UserAgent"""

    def __init__(self):
        super(UserAgent, self).__init__()

        self._u_agents = []
        self.__most_common_user_agents()

    def __most_common_user_agents(self):
        """Забираем c Useragents.me
        Огромное спасибо команде Useragents.me"""

        url = 'https://www.useragents.me/api'

        try:
            r = requests.get(url).json()
            self._u_agents = r['data']
        except Exception:
            pass

    def get_ua(self) -> str:
        if self._u_agents:
            return random.choice(self._u_agents)['ua']
        return U_A
