import pandas as pd

from marcuslion.config import api_version
from marcuslion.restcontroller import _RestController


class Datasets(_RestController):
    """
    MarcusLion Datasets class
        # $ curl 'https://qa1.marcuslion.com/core/datasets/search?providers=kaggle,usgov&title=bike'
    """

    def __init__(self):
        super().__init__(api_version + "/datasets")

    def list(self) -> pd.DataFrame:
        """
        Datasets.list()
        """
        return super().verify_get_data("", {})

    def search(self, search, provider_list) -> pd.DataFrame:
        """
        Datasets.search()
        """
        params = {"providers": provider_list, "title": search}

        return super().verify_get_data("search", params)

    def query(self, title) -> pd.DataFrame:
        """
        Datasets.query(ref)
        """
        return super().verify_get_data("search", {"title": title})

    def download(self, ref) -> pd.DataFrame:
        """
        Datasets.download(ref)
        """
        return super().verify_get("download", {"ref", ref})
