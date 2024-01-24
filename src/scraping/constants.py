# constants.py

# Email Patterns
EMAIL_PATTERNS = [
    "firstname.lastname",
    "lastname.firstname",
    "firstnamelastname",
    "lastnamefirstname",
    "firstname_lastname",
    "lastname_firstname",
    "firstname-lastname",
    "lastname-firstname",
    # Add more patterns as needed
]

# XPaths
LOGIN_BUTTON_XPATH = "/html/body/header/nav/div[3]/div[2]/a"
USERNAME_INPUT_XPATH = "//*[@id='ycid-input']"
PASSWORD_INPUT_XPATH = "//*[@id='password-input']"
SUBMIT_BUTTON_XPATH = "//*[@id='sign-in-card']/div[2]/div[8]/button/span[1]"

# Class Names
FOUNDER_NAME_CLASS = "mb-1.font-medium"
FOUNDER_IMAGE_CLASS = "ml-2.mr-2.h-20.w-20.rounded-full.sm:ml-5"
FOUNDER_DESCRIPTION_CLASS = "sm:text-md.w-full.text-sm"
FOUNDER_LINKEDIN_CLASS = "fa.fa-linkedin.ml-4.p-1.text-blue-600"

# Add more constants as needed
