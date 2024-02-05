# Test utility functions
import os
import time
from pathlib import Path

import pytest
from pydantic import BaseModel

from ycombinator_scraper.exceptions import InvalidURLException
from ycombinator_scraper.utils import (
    generate_csv_from_pydantic_data,
    get_output_filename,
    strip_html_tags,
    timed_cache,
    validate_company_url,
    validate_job_url,
    write_json_to_csv,
)


@timed_cache(seconds=2)
def mock_function(arg):
    return arg * 2


def test_timed_cache():
    # Initial call should compute and store the result
    result1 = mock_function(5)
    assert result1 == 10

    # Second call within 2 seconds should retrieve from cache
    result2 = mock_function(5)
    assert result2 == 10

    # Sleep for more than 2 seconds
    time.sleep(3)

    # Third call after expiration should compute and store the result again
    result3 = mock_function(5)
    assert result3 == 10


def test_get_output_filename():
    output_path = Path("subfolder")
    file_format = "txt"
    file_name = "output_file"
    company_name = "ABC"
    result = get_output_filename(output_path, file_format, file_name, company_name)
    expected_result = Path.cwd() / "output" / "subfolder" / "output_file_ABC.txt"
    assert result == expected_result


def test_strip_html_tags():
    html_content = "<p>This is <b>bold</b> text.</p>"
    result = strip_html_tags(html_content)
    expected_result = "This is bold text."
    assert result == expected_result


def test_write_json_to_csv():
    json_data = [{"name": "John", "age": 25}, {"name": "Alice", "age": 30}]
    csv_filename = "test_output.csv"
    write_json_to_csv(json_data, csv_filename)

    # Check if the file was created
    assert os.path.isfile(csv_filename)

    # Manually check the content of the file for correctness
    # (You can also read the file and assert specific content)
    # Cleanup: Remove the created file
    os.remove(csv_filename)


class Person(BaseModel):
    name: str
    age: int


def test_generate_csv_from_pydantic_data():
    data = [Person(name="John", age=25), Person(name="Alice", age=30)]
    file_path = "test_output_pydantic.csv"
    generate_csv_from_pydantic_data(data, file_path)

    # Check if the file was created
    assert os.path.isfile(file_path)

    # Manually check the content of the file for correctness
    # (You can also read the file and assert specific content)
    # Cleanup: Remove the created file
    os.remove(file_path)


def test_generate_csv_from_pydantic_data_with_empty_data():
    with pytest.raises(ValueError, match="Data list is empty"):
        generate_csv_from_pydantic_data([], "test_empty_data.csv")


def test_validate_job_url_valid():
    valid_url = "https://www.workatastartup.com/jobs/123"
    # This should not raise any exceptions
    validate_job_url(valid_url)


def test_validate_job_url_invalid():
    invalid_url = "https://www.workatastartup.com/companies/123"
    with pytest.raises(InvalidURLException):
        validate_job_url(invalid_url)


def test_validate_company_url_valid():
    valid_url = "https://www.workatastartup.com/companies/abc"
    # This should not raise any exceptions
    validate_company_url(valid_url)


def test_validate_company_url_invalid():
    invalid_url = "https://www.workatastartup.com/jobs/abc"
    with pytest.raises(InvalidURLException):
        validate_company_url(invalid_url)
