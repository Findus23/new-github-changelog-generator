# noinspection PyUnresolvedReferences
from tests.test_fixtures import *


def test_issues_can_be_read(issues):
    for issue in issues:
        assert issue.authors is not None


def test_test(issues):
    assert len([i for i in issues if i.closed_before_since]) == 3


def test_correct_included_issues(issues):
    correct = [13418, 13626, 13836, 13991, 14027]
    included = [i for i in issues if i.should_be_included]
    should_be_included = [i for i in issues if i.number in correct]
    assert included == should_be_included
