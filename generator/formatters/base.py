from typing import List

from generator import Issue


class BaseFormatter:
    def __init__(self, issues: List[Issue]):
        self.issues = issues

    def __str__(self) -> str:
        return ""
