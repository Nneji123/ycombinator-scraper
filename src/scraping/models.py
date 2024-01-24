from typing import List

from pydantic import BaseModel


class FounderData(BaseModel):
    founderName: str
    founderDescription: str
    founderImageUrl: str
    founderLinkedinUrl: str
    founderEmail: str

class CompanyData(BaseModel):
    companyName: str
    companyDescription: str
    companyTags: List
    companyImage: str
    companyLinks: List
    companyFounders: List[FounderData]
    jobDatas: List[JobData]

class JobData(BaseModel):
    jobDescription: str
    jobUrl: str
    jobTitle: str
    jobSalaryRange: str
    jobTags: List


class ScrapedData(BaseModel):
    scraped_data: List[CompanyData]
