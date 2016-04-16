import requests


class WebRequestService(object):

    # Disable the request warnings
    requests.packages.urllib3.disable_warnings()

    def get(self, url):
        return requests.get(url, verify=False)
