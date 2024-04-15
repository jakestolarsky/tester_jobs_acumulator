import json
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime


class JobScraper:
    def __init__(self, url, selectors, website_name):
        self.url = url
        self.selectors = selectors
        self.website_name = website_name
        self.jobs = []

    def fetch_jobs(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            scrape_date = datetime.now().strftime('%Y/%m/%d')
            for item in soup.find_all(self.selectors['container_tag'], self.selectors['container_attrs']):
                self.jobs.append(self.extract_job_details(item, scrape_date))
        else:
            print('Page content failed to download, status code:', response.status_code)

    def extract_job_details(self, item, scrape_date):
        link_offer = self.get_attr(item, 'link_offer', 'href')
        full_link = urljoin(self.url, link_offer)

        details = {
            'date': scrape_date,
            'website': self.website_name,
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

    def get_jobs_as_json(self):
        return json.dumps(self.jobs, ensure_ascii=False)

    def save_jobs_as_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.jobs, file, ensure_ascii=False, indent=4)

    def save_jobs_as_csv(self, filename):
        fieldnames = ['date', 'website', 'job_title', 'company', 'city', 'link_offer']
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for job in self.jobs:
                writer.writerow(job)