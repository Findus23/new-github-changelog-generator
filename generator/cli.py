from datetime import datetime, timedelta

from generator import generate_changelog


def main():
    since = datetime.today() - timedelta(5)

    generate_changelog(since)
