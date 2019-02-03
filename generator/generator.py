from datetime import datetime
from typing import List

from generator import GithubAPI, config, Issue, Repo
from generator.formatters import HTMLFormatter, MarkdownFormatter

api = GithubAPI(token=config.api_token)


def getissueorder(issue: Issue):
    order = 99
    for label in issue.labels:
        if label in config.sort_by_labels:
            order = config.sort_by_labels.index(label)
    return order, issue.number


def generate_statistics(repos: List[Repo]):
    unique_authors = set()
    num_issues = 0
    for repo in repos:
        for issue in repo.issues:
            num_issues += 1
            unique_authors.update(issue.authors)
    print("{num} Tickets closed by {contr} contributors".format(num=num_issues, contr=len(unique_authors)))


def generate_changelog(since: datetime, output_format, previous_version):
    if not since:
        releases = api.get_stable_releases(config.repositories[0])
        if previous_version:
            version = [rel for rel in releases if rel["tag_name"] == previous_version]
            if not version:
                raise ValueError("version '{}' could not be found".format(previous_version))
            version = version[0]
        else:
            version = releases[0]

        since = datetime.strptime(version["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        print("searching for issues since '{}' released on {}".format(version["tag_name"], since))
    else:
        print("searching for issues since {}".format(since))
    repos = []
    for repo_url in config.repositories:
        repo = Repo(repo_url)
        issues = api.fetch_issues_since(repo_url, since)
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
        repo.issues = issues
        repos.append(repo)

    if output_format == "html":
        print(HTMLFormatter(repos))
    elif output_format == "markdown":
        print(MarkdownFormatter(repos))
    else:
        raise ValueError()
    generate_statistics(repos)
