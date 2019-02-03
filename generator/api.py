from datetime import date
from typing import Iterable
from urllib.parse import urlencode
from warnings import warn

import requests

from generator import Event, Issue


class GithubAPI:
    BASE_URL = "https://api.github.com"

    def __init__(self, token=None):
        self.s = requests.Session()
        if token:
            self.s.headers.update({'Authorization': 'token {}'.format(token)})
        else:
            warn("use Token!", stacklevel=2)  # TODO

    def call(self, url, parameters=None):
        if "//" not in url:
            url = self.BASE_URL + url
            print(url + "?" + urlencode(parameters))
        else:
            print(url)
        r = self.s.get(url, params=parameters)
        if isinstance(r.json(), dict):
            yield r.json()
        else:
            yield from r.json()
            while "next" in r.links:
                print("fetching next page")
                r = self.s.get(r.links["next"]["url"])
                yield from r.json()

    def fetch_issues_since(self, repo, since: date) -> Iterable[Issue]:
        assert "/" in repo  # e.g. "matomo-org/matomo"
        path = "/repos/{}/issues".format(repo)
        params = {
            "state": "closed",
            "direction": "asc",
            "since": since.isoformat()
        }
        responses = self.call(path, params)
        for response in responses:
            yield Issue(response)

    def fetch_pr_details(self, pr: Issue) -> dict:
        data = list(self.call(pr.pr_url))[
            0]  # self.call is a generator even if there is only one result
        return data

    def fetch_events(self, issue: Issue) -> Iterable[Event]:
        responses = self.call(issue.events_url)
        for response in responses:
            yield Event(response)
