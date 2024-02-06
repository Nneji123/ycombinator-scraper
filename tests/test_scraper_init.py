from selenium import webdriver


def test_initialize_driver(scraper):
    driver = scraper._initialize_driver()

    # Check if the returned object is an instance of webdriver.Chrome
    assert isinstance(driver, webdriver.Chrome)


# TODO: Write tests for saving and loading cookies.
