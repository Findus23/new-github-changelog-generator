import argparse
from datetime import datetime, timedelta

from generator import generate_changelog


def parsed_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def main():
    since = datetime.today() - timedelta(5)

    parser = argparse.ArgumentParser(description='Generate changelogs from closed GitHub issues and merged PRs.')
    sincegroup = parser.add_mutually_exclusive_group()

    sincegroup.add_argument('--since', metavar='"YYYY-MM-DD HH:MM:SS"', type=parsed_date,
                            help='date of previous release')
    sincegroup.add_argument('--previous-version', type=str)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--html', action='store_const', const="html", dest="output", help="output as HTML")
    group.add_argument('--markdown', action='store_const', const="markdown", dest="output", help="output as markdown")
    group.add_argument('--debian-changelog', action='store_const', const="debianchangelog", dest="output",
                       help="output as debian changelog file")

    args = parser.parse_args()
    generate_changelog(args.since, args.output, args.previous_version)
