import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class JobScraper:
    def __init__(self, url, selectors):
        self.url = url
        self.selectors = selectors
        self.jobs = []

    def fetch_jobs(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.find_all(self.selectors['container_tag'], self.selectors['container_attrs']):
                self.jobs.append(self.extract_job_details(item))
        else:
            print('Page content failed to download, status code:', response.status_code)

    def extract_job_details(self, item):
        link_offer = self.get_attr(item, 'link_offer', 'href')
        full_link = urljoin(self.url, link_offer)

        details = {
            'job_title': self.get_text(item, 'job_title'),
            'company': self.get_text(item, 'company'),
            'city': self.get_text(item, 'city'),
            'link_offer': full_link,
        }
        return details

    def get_text(self, item, key):
        element = item.find(self.selectors[key]['tag'], attrs=self.selectors[key]['attrs'])
        return element.text if element else "No " + key

    def get_attr(self, item, key, attr_name):
        if not self.selectors[key]['tag']:
            return item.get(attr_name) if item.has_attr(attr_name) else "No " + key

        element = item.find(self.selectors[key]['tag'], attrs=self.selectors[key]['attrs'])
        return element.get(attr_name) if element else "No " + key

    def print_jobs(self):
        for job in self.jobs:
            print(job)