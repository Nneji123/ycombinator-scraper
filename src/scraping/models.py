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
    founderName: str
    founderDescription: str
    founderImageUrl: str
    founderLinkedinUrl: str
    founderEmails: List[str]

class JobData(BaseSchema):
    jobDescription: str
    jobUrl: str
    jobTitle: str
    jobSalaryRange: str
    jobTags: List[str]

class CompanyData(BaseSchema):
    companyName: str
    companyDescription: str
    companyTags: List[str]
    companyImage: str
    companyLinks: List[str]
    companyFounders: List[FounderData]
    jobDatas: List[JobData]

class ScrapedData(BaseSchema):
    scraped_data: List[CompanyData]
