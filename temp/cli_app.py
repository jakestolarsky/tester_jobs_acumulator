import json
from app.logic.job_scraper import JobScraper

def load_config(path):
    with open(path, 'r') as file:
        return json.load(file)

def main(config_path):
    config = load_config(config_path)
    for site in config['sites']:
        print(f"Scraping {site['name']}...")
        scraper = JobScraper(site['url'], site['selectors'])
        scraper.fetch_jobs()
        scraper.print_jobs()

if __name__ == "__main__":
    main("project/config/job_sites.json")