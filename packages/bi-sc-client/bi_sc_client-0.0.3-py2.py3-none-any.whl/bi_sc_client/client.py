import os
import urllib

import requests

from bi_sc_client.errors import ErrorApiResponse


class BISomConnexioClient:
    def __init__(self):
        self.url = os.getenv("BI_URL")

    def send_request(self, method, path, content, headers={}):
        headers.update({"accept": "application/json"})

        url = urllib.parse.urljoin(self.url, path)

        if method == "GET":
            response = requests.get(
                url=url,
                params=content,
                headers=headers,
            )
        elif method == "POST":
            response = requests.post(
                url=url,
                data=content,
                headers=headers,
            )

        if not response.ok or response.status_code != 200:
            raise ErrorApiResponse(response.text)
        return response
