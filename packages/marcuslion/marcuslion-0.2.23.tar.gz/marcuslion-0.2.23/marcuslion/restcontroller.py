import json
import urllib
import pandas as pd
import urllib3
import io

from marcuslion.config import base_url, api_key


class _RestController:
    """
    MarcusLion RestController class
    """
    __http = urllib3.PoolManager()

    def __init__(self, url):
        self.url = base_url + url

    def _prepare_params(self, action, params):
        s = self.url
        if action:
            s = s + '/' + action

        if params:
            s = s + '?' + urllib.parse.urlencode(params)

        return s

    def verify_get_frame(self, action, params) -> pd.DataFrame:
        response = self.verify_get(action, params)
        return pd.DataFrame.from_records(response)

    def verify_get(self, action, params) -> any:
        full_url = self._prepare_params(action, params)

        # Sending a GET request and getting back response as HTTPResponse object.
        resp = self.__http.request("GET", full_url, headers={
            'X-MARCUSLION-API-KEY': api_key
        })
        if resp.status == 401:
            raise ValueError("401: Unauthorized User. URL:" + full_url)
        if resp.status != 200:
            raise ValueError("status: " + full_url + " -> " + (
                str(resp.status) + (" data: " + resp.data.decode()) if resp.data else ""))

        data_str = resp.data.decode()
        if len(data_str) == 0:
            return None
        return json.loads(data_str)

    def verify_get_data(self, action, params) -> pd.DataFrame:
        full_url = self._prepare_params(action, params)

        resp = self.__http.request("GET", full_url, headers={
            'X-MARCUSLION-API-KEY': api_key
        })
        if resp.status == 401:
            raise ValueError("401: Unauthorized User. URL:" + full_url)
        if resp.status != 200:
            raise ValueError("status: " + full_url + " -> " + (
                str(resp.status) + (" data: " + resp.data.decode()) if resp.data else ""))

        string_io = io.StringIO(resp.data.decode())
        data = json.load(string_io)
        df = pd.DataFrame(data['data'])
        return df
