from typing import List, Dict
import asyncio
import aiohttp

class JobScraper:
    def __init__(self):
        self.timeout = 10.0
        self.rapidapi_key = "a4f9989c32msha69e9cb52daebfep11d58cjsn850bc3061ad9"
        self.rapidapi_host = "jsearch.p.rapidapi.com"
        self.searchapi_key =  "5LqrF9m8eiaqxymCGMaBo793"
        self.theirstackapi_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrb2xpeTYxODIwQGZlcm1pcm8uY29tIiwicGVybWlzc2lvbnMiOiJ1c2VyIiwiY3JlYXRlZF9hdCI6IjIwMjUtMTEtMTJUMDg6NTc6NTEuNjg5OTUzKzAwOjAwIn0.vZJ0VsgvqYLS319jzUDhIzE0KyMyc-yyar_QMDHiLwo"

    async def fetch_google_jobs(self, job_title: str, location: str = "India") -> List[Dict]:
        """Fetch Google Jobs using SearchAPI.io"""
        jobs = []
        url = "https://www.searchapi.io/api/v1/search"
        querystring = {
            "engine": "google_jobs",
            "q": f"{job_title} in {location}",
            "api_key": self.searchapi_key
        }

        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.get(url, params=querystring) as response:
                    if response.status != 200:
                        print(f"Google Jobs API error {response.status}: {await response.text()}")
                        return jobs

                    data = await response.json()
                    
                    results = data.get("jobs", [])
                    
                    for job in results:
                        jobs.append({
                            "title": job.get("title"),
                            "company": job.get("company_name") or job.get("company"),
                            "location": job.get("location"),
                            "description": job.get("description") or job.get("extensions"),
                            "url": job.get("apply_link") or job.get("related_links", [{}])[0].get("link"),
                            "source": "Google Jobs (SearchAPI.io)"
                        })

        except Exception as e:
            print(f"Google Jobs fetch error: {e}")

        return jobs

    async def fetch_rapidapi_jobs(self, job_title: str, location: str = "us") -> List[Dict]:
        """Fetch jobs from RapidAPI JSearch"""
        jobs = []
        url = "https://jsearch.p.rapidapi.com/search"
        querystring = {
            "query": f"{job_title} jobs",
            "page": "1",
            "num_pages": "1",
            "country": location,
            "date_posted": "all"
        }

        headers = {
            "x-rapidapi-key": self.rapidapi_key,
            "x-rapidapi-host": self.rapidapi_host
        }
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.get(url, headers=headers, params=querystring) as response:
                    data = await response.json()
                    
                    for item in data.get("data", []):
                        jobs.append({
                            "title": item.get("job_title"),
                            "company": item.get("employer_name"),
                            "location": item.get("job_city"),
                            "description": item.get("job_description"),
                            "url": item.get("job_apply_link"),
                            "source": "RapidAPI JSearch"
                        })
            
        except Exception as e:
            print(f"RapidAPI fetch error: {e}")
        return jobs

    async def fetch_theirstack_jobs(self, job_title: str, location: str = "IN") -> List[Dict]:
        """Fetch jobs using TheirStack Jobs API with project-specific defaults"""
        jobs = []
        url = "https://api.theirstack.com/v1/jobs/search"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        # Default payload from your project, with dynamic job_title and location
        payload = {
            "order_by": [
                {"desc": True, "field": "date_posted"},
                {"desc": True, "field": "discovered_at"}
            ],
            "offset": 0,
            "page": 0,
            "limit": 25,
            "job_title_or": [job_title],
            "job_country_code_or": ["US"],
            "posted_at_max_age_days": 7,
            "job_description_pattern_is_case_insensitive": True,
            "blur_company_data": False,
            "include_total_results": False
        }

        params = {
        "token": self.theirstackapi_key
        }

        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(url, headers=headers, json=payload, params=params) as response:
                    if response.status != 200:
                        print(f"TheirStack API error {response.status}: {await response.text()}")
                        return jobs

                    data = await response.json()
                    results = data.get("data", [])

                    for item in results:
                        jobs.append({
                            "title": item.get("job_title"),
                            "company": item.get("company") or (item.get("company_object") or {}).get("name"),
                            "location": item.get("location") or (item.get("locations")[0]["display_name"] if item.get("locations") else None),
                            "description": item.get("description"),
                            "url": item.get("source_url") or item.get("url"),
                            "source": "TheirStack"
                        })

        except Exception as e:
            print(f"TheirStack fetch error: {e}")

        return jobs


    async def fetch_all_jobs(self, job_title: str, location: str = "us") -> List[Dict]:
        """Fetch jobs from all sources concurrently"""
        tasks = [
            self.fetch_theirstack_jobs(job_title, location), 
            self.fetch_google_jobs(job_title, location), 
            self.fetch_rapidapi_jobs(job_title, location) 
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_jobs = []
        for result in results:
            if isinstance(result, list):
                all_jobs.extend(result)

        print(f"Total jobs fetched: {len(all_jobs)}")
        return all_jobs

job_scraper = JobScraper()