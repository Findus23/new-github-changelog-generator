from datetime import timedelta, datetime

from generator.api import GithubAPI
from generator.config import config
from generator.issue import Issue

api = GithubAPI(token=config.api_token)


def getissueorder(issue: Issue):
    order = 99
    for label in issue.labels:
        if label in config.sort_by_labels:
            order = config.sort_by_labels.index(label)
    return order, issue.number


def generate_changelog():
    since = datetime.today() - timedelta(3)
    issues = api.fetch_issues_since("matomo-org/matomo", since)
    issues = list(issues)  # enumerate iterable
    for issue in issues:
        if issue.pull_request:
            print("PR")
            issue.add_pr_data(api.fetch_pr_details(issue))
        issue.compare_close_date(since)
    issues = [i for i in issues if i.should_be_included]  # remove all filtered issues
    for issue in issues:
        issue.add_events_data(api.fetch_events())
    issues.sort(key=getissueorder)
    for i in issues:
        print("#{}: {} ({})".format(i.number, i.title, ", ".join(i.labels)))
