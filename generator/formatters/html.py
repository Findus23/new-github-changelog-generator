import html

from generator.formatters import BaseFormatter


class HTMLFormatter(BaseFormatter):

    def __str__(self) -> str:
        text = "<div>\n"
        for issue in self.issues:
            text += "\t<li><a href='{url}'>#{id}</a> {title}</li>".format(
                url=issue.url,
                id=issue.number,
                title=html.escape(issue.title)
            )
            if issue.authors:
                text += " [by {}]".format(
                    ", ".join(
                        "<a href='{url}'>@{name}</a>".format(
                            url=author.profile_url,
                            name=html.escape(author.username)
                        ) for author in issue.authors
                    )
                )
            text += "\n"
        text += "</div>"
        return text
