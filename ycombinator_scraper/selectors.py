"""Selectors and Class names for Ycombinator-Scraper Tool"""

# CLASS NAMES FOR LOGIN
LOGIN_BUTTON_XPATH = "/html/body/header/nav/div[3]/div[2]/a"
USERNAME_INPUT_XPATH = "//*[@id='ycid-input']"
PASSWORD_INPUT_XPATH = "//*[@id='password-input']"
SUBMIT_BUTTON_XPATH = "//*[@id='sign-in-card']/div[2]/div[8]/button/span[1]"

# CLASS NAMES FOR FOUNDERS
FOUNDER_NAME_CLASS = "mb-1.font-medium"
FOUNDER_IMAGE_CLASS = "ml-2.mr-2.h-20.w-20.rounded-full.sm\:ml-5"
FOUNDER_DESCRIPTION_CLASS_ONE = "sm\:text-md.text-sm"
FOUNDER_DESCRIPTION_CLASS_TWO = "sm\:text-md.w-full.text-sm"
FOUNDER_LINKEDIN_CLASS = "fa.fa-linkedin.ml-4.p-1.text-blue-600"

# CLASS NAMES FOR COMPANY_DATA
COMPANY_IMAGE_CLASS = "mt-2.sm\:w-28"
COMPANY_NAME_CLASS = "company-name.hover\:underline"
COMPANY_DESCRIPTION_CLASS_ONE = "sm\:text-md.prose.col-span-11.mx-5.max-w-none.text-sm"
COMPANY_DESCRIPTION_CLASS_TWO = "mt-3.text-gray-700"
COMPANY_TAGS_CLASS = "detail-label.text-sm"
COMPANY_JOB_CLASS = "font-medium.text-gray-900.hover\:underline.sm\:text-lg"
COMPANY_SOCIAL_CLASS = "text-blue-600.ellipsis"


# CLASS NAMES FOR JOB_DATA
JOB_TITLE_CLASS = "company-name.text-2xl.font-bold"
JOB_TAGS_CLASS = "company-details.my-2.flex.flex-wrap.md\:my-0"
SALARY_RANGE_CLASS = "text-gray-500.my-2"
JOB_DESCRIPTION_CLASS = "prose"


# CLASS NAMES FOR JOB_URLS
