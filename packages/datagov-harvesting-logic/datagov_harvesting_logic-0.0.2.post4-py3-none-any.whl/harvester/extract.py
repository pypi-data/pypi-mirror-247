import requests
from requests.exceptions import RequestException, JSONDecodeError

import logging

logger = logging.getLogger("harvester")


def download_dcatus_catalog(url):
    """download file and pull json from response
    url (str)   :   path to the file to be downloaded.
    """
    try:
        resp = requests.get(url)
    except RequestException as e:
        return Exception(e)
    except JSONDecodeError as e:
        return Exception(e)

    if resp.status_code != 200:
        return Exception("non-200 status code")

    try:
        return resp.json()
    except JSONDecodeError as e:
        return Exception(e)


def extract(harvest_source) -> list:
    """Extracts all records from a harvest_source"""
    logger.info("Hello from harvester.extract()")

    datasets = []

    # stub

    return datasets
