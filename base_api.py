from typing import Union

import requests
from fake_useragent import UserAgent
from requests.exceptions import HTTPError


class BaseApi:

    def _call_api(self, url) -> Union[HTTPError, dict]:
        # user_agent = UserAgent()
        headers = headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return e

        return response.json()
