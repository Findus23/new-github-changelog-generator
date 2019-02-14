# github-changelog-generator

*quickly generate changelogs based on closed github issues and merged PRs since the last release*

## Install

```bash
pip3 install --user https://github.com/Findus23/new-github-changelog-generator/archive/master.zip
```
(at least until it is published on pypi)

## Usage

Run `github-changelog-generator init` to create an example config file.
The GitHub API limits to 60 requests per hour by default, so to use this properly, create a [*personal access token*](https://github.com/settings/tokens) (you don't need to tick any box) and paste it into the `api_token` setting in the config file.

Afterwards you can simply create changelogs by specifying the tag or date of the previous release:

```bash
 github-changelog-generator generate --since "2019-01-25 00:00:00" --debian-changelog
 
 github-changelog-generator generate --previous-version="3.8.0" --html
 ```
 
 You can find more options with `--help`:
 
 ```bash
 github-changelog-generator --help
 github-changelog-generator init --help
 github-changelog-generator generate --help
 ```