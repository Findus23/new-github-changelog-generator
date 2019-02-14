import json
from datetime import datetime

import pytest

from generator import Issue


def load_json(path):
    with open(path) as file:
        return json.load(file)


@pytest.fixture
def issues(request):
    issues = []
    for i in load_json(request.fspath.join('../api_responses/').join("issues.json")):
        issue = Issue(i)
        issue.compare_close_date(datetime.strptime("2019-01-25 00:00:00", "%Y-%m-%d %H:%M:%S"))
        issues.append(issue)
    return issues
