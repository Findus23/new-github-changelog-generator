class Repo(object):
    BASE_URL = "https://github.com/"

    def __init__(self, path):
        self.path = path
        self.issues = []

    @property
    def absolute_url(self):
        return self.BASE_URL + self.path
