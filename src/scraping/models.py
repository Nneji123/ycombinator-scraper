from typing import List
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

class FounderData(BaseSchema):
    founder_name: str
    founder_description: str
    founder_image_url: str
    founder_linkedin_url: str
    founder_emails: List[str]

class JobData(BaseSchema):
    job_description: str
    job_url: str
    job_title: str
    job_salary_range: str
    job_tags: List[str]

class CompanyData(BaseSchema):
    company_name: str
    company_description: str
    company_tags: List[str]
    company_image: str
    company_links: List[str]
    company_founders: List[FounderData]
    job_datas: List[JobData]

class ScrapedData(BaseSchema):
    scraped_data: List[CompanyData]