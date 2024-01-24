from typing import List

from pydantic import BaseModel


class FounderDetails(BaseModel):
    founder_name: str
    profile_image_url: str
    linkedin_url: str


class JobData(BaseModel):
    company_name: str
    job_description: str
    founders_details: List[FounderDetails]


class ScrapeResult(BaseModel):
    scraped_data: List[JobData]
    job_links: List[str]
