import io
import urllib
import urllib3

import pandas as pd

from marcuslion.config import base_url, api_key, api_version
from marcuslion.restcontroller import _RestController


class Documents(_RestController):
    """
    MarcusLion Documents class
    """

    def __init__(self):
        super().__init__(api_version + "")

    def list(self) -> pd.DataFrame:
        """
        Documents.list()
        """
        url = base_url + api_version + "/" + 'core/documents/list?'
        params = {}
        full_url = url + urllib.parse.urlencode(params)

        # Sending a GET request and getting back response as HTTPResponse object.
        http = urllib3.PoolManager()
        resp = http.request("GET", full_url, headers={
            'X-API-KEY': api_key
        })
        if resp.status != 200:
            raise ValueError("status: " + url + " -> " + str(resp.status))

        # converting
        string_io = io.StringIO(resp.data.decode())
        return pd.read_json(string_io)

    def query(self, ref):
        """
        Documents.query(ref)
        """
        pass

    def search(self, search) -> pd.DataFrame:
        """
        Documents.search(search)
        """
        pass

    def download(self, ref) -> pd.DataFrame:
        """
        Providers.download(ref)
        """
        pass
