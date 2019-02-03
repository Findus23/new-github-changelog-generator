import html

from generator.formatters import BaseFormatter


class HTMLFormatter(BaseFormatter):

    def __str__(self) -> str:
        text = "<div>\n"
        for repo in self.repos:
            if repo.issues:
                if len(self.repos) > 1:
                    text += "<h3><a href='{}'>{}</a></h3>\n".format(repo.absolute_url, repo.path)
                text += "<ul>\n"
                for issue in repo.issues:
                    text += "\t<li><a href='{url}'>#{id}</a> {title}".format(
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
                    text += "</li>\n"
                text += "</ul>"
        text += "</div>"
        return text
