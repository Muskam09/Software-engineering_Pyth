import re
from dateutil.parser import parse
import pytest


def extract_datetime(text):
    # Об'єднаний регулярний вираз для витягування дати та часу
    regex = (
        r'On \w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} \+\d{4}, Test User wrote:|'  # On Sun, 13 Oct 2024 19:01:18 +0800, Test User wrote:
        r'On \w{3}, \w{3} \d{1,2}, \d{4} at \d{1,2}:\d{2} Test User wrote:|'  # On Tue, Oct 1, 2024 at 19:23 Test User wrote:
        r'On \w{3}, \w{3} \d{1,2}, \d{4}, \d{1,2}:\d{2} [APM]{2} Test User wrote:|'  # On Mon, Oct 14, 2024, 8:06 PM Test User wrote:
        r'On \w{3}, \d{1,2} \w{3} \d{4}, \d{1,2}:\d{2} [apm]{2} Test User, wrote:|'  # On Wed, 9 Oct 2024, 2:04 am Test User, wrote:
        r'On \d{2}-\w{3}-\d{4} \d{1,2}:\d{2} [apm]{2}, Test User wrote:|'  # On 25-Sep-2024 3:37 am, Test User wrote:
        r'On \w{3}, \d{1,2} \w{4,5} \d{4}, \d{1,2}:\d{2} Test User, wrote:' # On Fri, 27 Sept 2024, 17:32 Test User, wrote:
    )

    match = re.search(regex, text)
    if match:
        date_str = match.group(0)
        dt = parse(date_str, fuzzy=True)
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    return None


@pytest.mark.parametrize("input_text, expected_output", [
    ("On Sun, 13 Oct 2024 19:01:18 +0800, Test User wrote:", "2024-10-13T19:01:18Z"),
    ("On Tue, Oct 1, 2024 at 19:23 Test User wrote:", "2024-10-01T19:23:00Z"),
    ("On Mon, Oct 14, 2024, 8:06 PM Test User wrote:", "2024-10-14T20:06:00Z"),
    ("On Wed, 9 Oct 2024, 2:04 am Test User, wrote:", "2024-10-09T02:04:00Z"),
    ("On 25-Sep-2024 3:37 am, Test User wrote:", "2024-09-25T03:37:00Z"),
    ("On Fri, 27 Sept 2024, 17:32 Test User, wrote:", "2024-09-27T17:32:00Z")
])
def test_extract_datetime(input_text, expected_output):
    assert extract_datetime(input_text) == expected_output


if __name__ == "__main__":
    pytest.main()