import json
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

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
        config = load_config(r"E:\my\tester_jobs_acumulator\project\config\job_sites.json")
        all_jobs = []
        for site in config['sites']:
            scraper = JobScraper(site['url'], site['selectors'])
            scraper.fetch_jobs()
            all_jobs.extend(scraper.jobs)  # Zbieranie wszystkich ofert pracy
        return all_jobs  # Zwracanie ofert pracy jako JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))