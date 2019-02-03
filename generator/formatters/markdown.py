import html

from generator.formatters import BaseFormatter


class MarkdownFormatter(BaseFormatter):

    def __str__(self) -> str:
        text = ""
        for repo in self.repos:
            if repo.issues:
                if len(self.repos) > 1:
                    text += "### [{}]({})\n".format(repo.path, repo.absolute_url)
                for issue in repo.issues:
                    text += "  - [#{id}]({url}) {title}".format(
                        url=issue.url,
                        id=issue.number,
                        title=html.escape(issue.title)
                    )
                    if issue.authors:
                        text += " [by {}]".format(
                            ", ".join(
                                "[@{name}]({url})".format(
                                    url=author.profile_url,
                                    name=html.escape(author.username)
                                ) for author in issue.authors
                            )
                        )
                    text += "\n"
        return text
