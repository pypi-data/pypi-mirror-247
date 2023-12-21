import requests


class ProximalClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.proximal.energy"

    def get_root(self):
        url = self.base_url
        return requests.get(url)

    def get_projects(self):
        url = self.base_url + "/v1/projects"
        return requests.get(url, headers={"x-api-key": self.api_key})
