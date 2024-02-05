"""Custom Exception handlers"""


class InvalidURLException(Exception):
    """Invalid url exception for workatastartup.com"""

    def __init__(self, url):
        self.url = url
        super().__init__(
            f'The provided URL "{url}" does not match the expected pattern.'
        )
