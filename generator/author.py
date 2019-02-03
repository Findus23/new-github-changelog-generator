class Author:
    def __init__(self, api: dict):
        self.username = api["login"]
        self.profile_url = api["html_url"]

    def __repr__(self):
        return "<Author '{}'>".format(self.username)

    def __hash__(self):
        return hash(self.username)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        
        return self.username == other.username
