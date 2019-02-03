from datetime import date, datetime
from typing import List

from generator import Author, config


class Issue():
    def __init__(self, api):
        self.number = api["number"]  # type:int
        self.title = api["title"]  # type:str
        self.url = api["url"]  # type:str
        self.labels = [l["name"] for l in api["labels"]]  # type:List[str]
        self.closed_at = datetime.strptime(api["closed_at"], "%Y-%m-%dT%H:%M:%SZ")
        self.pull_request = "pull_request" in api
        self.events_url = api["events_url"]
        if self.pull_request:
            self.pr_url = api["pull_request"]["url"]

        self.closed_before_since = None  # type:bool
        self.merged = None  # type:bool
        self.authors = set()  # type:set
        self.creator = Author(api["user"])
        self.authors.add(self.creator)

    def __repr__(self):
        return "<Issue #{}>".format(self.number)

    def add_pr_data(self, api):
        self.merged = "merged_at" in api

    def compare_close_date(self, since: date):
        self.closed_before_since = self.closed_at < since

    def add_author(self, author: Author):
        self.authors.add(author)

    @property
    def has_ignored_label(self) -> bool:
        return not config.labels_to_ignore.isdisjoint(self.labels)

    @property
    def should_be_included(self) -> bool:
        if self.has_ignored_label:
            return False
        if self.closed_before_since:
            return False
        if self.pull_request and not self.merged:
            return False
        return True
