from typing import List
from pydantic import BaseModel

class FounderData(BaseModel):
    founderName: str
    founderDescription: str
    founderImageUrl: str
    founderLinkedinUrl: str
    founderEmails: List[str]

class JobData(BaseModel):
    jobDescription: str
    jobUrl: str
    jobTitle: str
    jobSalaryRange: str
    jobTags: List[str]

class CompanyData(BaseModel):
    companyName: str
    companyDescription: str
    companyTags: List[str]
    companyImage: str
    companyLinks: List[str]
    companyFounders: List[FounderData]
    jobDatas: List[JobData]

class ScrapedData(BaseModel):
    scraped_data: List[CompanyData]
