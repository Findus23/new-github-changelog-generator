from generator.author import Author


class Event:
    def __init__(self, api: dict):
        self.event = api["event"]
        self.actor = api["actor"]
        self.has_commit_id = bool(api["commit_id"])

    @property
    def contributed_event(self) -> bool:
        return self.event in ["closed", "assigned", "merged"]

    @property
    def referenced(self) -> bool:
        return self.event in ["referenced", "closed"]

    @property
    def author_should_be_listed(self) -> bool:
        if not self.contributed_event:
            return False
        if self.referenced and not self.has_commit_id:
            return False

        return True

    @property
    def author(self) -> Author:
        return Author(self.actor)
