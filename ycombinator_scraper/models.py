from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class FounderData(BaseSchema):
    founder_name: str = ""
    founder_description: str = ""
    founder_image_url: str = ""
    founder_linkedin_url: str = ""
    founder_emails: Optional[List[str]]


class JobData(BaseSchema):
    job_url: str = ""
    job_title: str = ""
    job_salary_range: str = ""
    job_tags: List[str] = []
    job_description: str = ""


class CompanyData(BaseSchema):
    company_name: str = ""
    company_url: str = ""
    company_description: str = ""
    company_tags: List[str] = []
    company_image: str = ""
    company_social_links: List[str] = []
    company_job_links: List[str] = []
    company_founders: List[FounderData] = []
    job_data: List[JobData] = []


class ScrapedData(BaseSchema):
    scraped_data: List[CompanyData]
