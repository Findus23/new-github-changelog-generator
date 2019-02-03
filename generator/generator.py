from datetime import datetime

from generator import GithubAPI, config, Issue
from generator.formatters import MarkdownFormatter

api = GithubAPI(token=config.api_token)


def getissueorder(issue: Issue):
    order = 99
    for label in issue.labels:
        if label in config.sort_by_labels:
            order = config.sort_by_labels.index(label)
    return order, issue.number


def generate_changelog(since: datetime):
    issues = api.fetch_issues_since("matomo-org/matomo", since)
    issues = list(issues)  # enumerate iterable
    for issue in issues:
        if issue.pull_request:
            issue.add_pr_data(api.fetch_pr_details(issue))
        issue.compare_close_date(since)
    issues = [i for i in issues if i.should_be_included]  # remove all filtered issues
    for issue in issues:
        for event in api.fetch_events(issue):
            if event.author_should_be_listed:
                issue.authors.add(event.author)

    issues.sort(key=getissueorder)
    print(MarkdownFormatter(issues))
