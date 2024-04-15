import json
import uvicorn
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.logic.job_scraper import JobScraper


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_config(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/scrape/")
async def scrape_jobs():
    try:
        config = load_config("config/job_sites.json")
        all_jobs = []
        for site in config['sites']:
            scraper = JobScraper(site['url'], site['selectors'], site['name'])
            scraper.fetch_jobs()
            all_jobs.extend(scraper.jobs)  # Zbieranie wszystkich ofert pracy
        return all_jobs  # Zwracanie ofert pracy jako JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download_offers/json")
async def download_json():
    try:
        config = load_config("config/job_sites.json")
        all_jobs = []
        for site in config['sites']:
            scraper = JobScraper(site['url'], site['selectors'], site['name'])
            scraper.fetch_jobs()
            all_jobs.extend(scraper.jobs)
        filename = 'jobs_{date}.json'.format(date=datetime.now().strftime("%Y-%m-%d_%H-%M"))
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(all_jobs, f, ensure_ascii=False, indent=4)
        return FileResponse(path=filename, filename=filename, media_type='application/json')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))