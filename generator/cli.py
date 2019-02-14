import argparse
import sys
from datetime import datetime
from os import path
from os.path import expanduser
from shutil import copyfile

import pkg_resources

from generator import generate_changelog, config


def parsed_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def initfile(globally: bool):
    home = expanduser("~")
    targetfile = home + "/.config/github-changelog-generator.yaml" if globally else "./github-changelog-generator.yaml"
    if path.exists(targetfile):
        sys.exit("The config file at '{path}' already exists.".format(path=targetfile))
    default_config_file = pkg_resources.resource_filename('generator', 'defaultconfig.yaml')
    copyfile(default_config_file, targetfile)
    print("An example config has been copied to '{path}'. \n".format(path=targetfile) +
          "Please edit it to your use case and don't forget to add a GitHub api_token to not run into rate limits.")


def main():
    parser = argparse.ArgumentParser(description='Generate changelogs from closed GitHub issues and merged PRs.')
    subparsers = parser.add_subparsers(dest="command",required=True)

    init = subparsers.add_parser("init")
    init.add_argument("--global", dest="globally", action='store_true', help="store config file in ~/.config/")
    init.set_defaults(globally=False)
    generate = subparsers.add_parser("generate")
    sincegroup = generate.add_mutually_exclusive_group()

    sincegroup.add_argument('--since', metavar='"YYYY-MM-DD HH:MM:SS"', type=parsed_date,
                            help='date of previous release')
    sincegroup.add_argument('--previous-version', type=str)
    group = generate.add_mutually_exclusive_group(required=True)
    group.add_argument('--html', action='store_const', const="html", dest="output", help="output as HTML")
    group.add_argument('--markdown', action='store_const', const="markdown", dest="output", help="output as markdown")
    group.add_argument('--debian-changelog', action='store_const', const="debianchangelog", dest="output",
                       help="output as debian changelog file")

    args = parser.parse_args()

    if args.command == "init":
        initfile(args.globally)
    elif args.command == "generate":
        if config.api_token == "none_found":
            sys.exit("no config file found\nPlease create one by running\n"
                     "github-changelog-generator init")
        generate_changelog(args.since, args.output, args.previous_version)
    else:
        raise ValueError("invalid subcommand")
