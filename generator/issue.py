from datetime import date, datetime
from typing import List

from generator.config import config


class Issue():
    closed_before_since = None

    def __init__(self, api):
        self.number = api["number"]  # type:int
        self.title = api["title"]  # type:str
        self.url = api["url"]  # type:str
        self.labels = [l["name"] for l in api["labels"]]  # type:List[str]
        self.closed_at = datetime.strptime(api["closed_at"], "%Y-%m-%dT%H:%M:%SZ")
        self.pull_request = "pull_request" in api
        if self.pull_request:
            self.pr_url = api["pull_request"]["url"]

    def add_pr_data(self, api):
        print(api)
        pass

    def add_events_data(self, api):
        pass

    def compare_close_date(self, since: date):
        self.closed_before_since = self.closed_at < since

    @property
    def has_ignored_label(self) -> bool:
        return not config.labels_to_ignore.isdisjoint(self.labels)

    @property
    def should_be_included(self) -> bool:
        return not self.has_ignored_label and not self.closed_before_since

    @property
    def pull_request_closed(self) -> bool:
        return self.pull_request and False  # TODO: add merged status from details
