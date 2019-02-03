from typing import List

from generator import Repo


class BaseFormatter:
    def __init__(self, repos: List[Repo]):
        self.repos = repos

    def __str__(self) -> str:
        return ""
