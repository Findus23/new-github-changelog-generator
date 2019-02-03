import textwrap

from generator.formatters import BaseFormatter


class DebianChangelogFormatter(BaseFormatter):
    def __str__(self) -> str:
        text = ""
        for repo in self.repos:
            if repo.issues:
                if len(self.repos) > 1:
                    text += "\n  [ {} ]\n".format(repo.path)
                for issue in repo.issues:
                    line = ""
                    line += "  * {title}".format(title=issue.title)
                    if issue.authors:
                        line += " [by {}] ".format(
                            ", ".join("@" + author.username for author in issue.authors)
                        )
                    line += "(Closes: #{})\n".format(issue.number)
                    text += textwrap.fill(line, 75, subsequent_indent=" " * 4) + "\n"
        return text
