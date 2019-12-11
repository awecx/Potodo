import re
import requests

from subprocess import check_output


def get_repo_url() -> str:
    """
    Tries to get the repository url from git commands
    """
    url: str = str(check_output("git remote get-url --all upstream"))
    if "fatal" in url:
        url = str(check_output("git remote get-url --all origin"))
    if "fatal" in url:
        # If the commands didn't work
        raise ValueError(
            f"Unknown error. `git get-url --all upstream|origin` returned {url}"
        )
    return url


def get_repo_name() -> str:
    """
    Will get the repository url from git commands then remove useless stuff to get ORG/NAME
    """
    repo_url: str = get_repo_url()
    # Removes useless stuff. If it isn't there then nothing happens
    repo_url = repo_url.strip("https://github.com/")
    repo_url = repo_url.strip("git@github.com:")
    repo_name = repo_url.strip(".git")
    return repo_name


def get_reservation_list():
    resp = requests.get(
        "https://api.github.com/repos/" + get_repo_name() + "/issues?state=open"
    )
    issues = resp.json()

    if resp.headers.get('Link'):
        link = resp.headers.get('Link')
        last_page = link.split(">")[0]
        for page in range(2, int(last_page) + 1):
            resp = requests.get(
                "https://api.github.com/repos/" + "python/python-docs-fr" + "/issues?state=open&page={}".format(page)
            )
            issues + resp.json()

    reservations = {}

    for issue in issues:
        if yes := re.search(r'\w*/\w*\.po', issue['title']):
            reservations[yes.group()] = issue['user']['login']

    return reservations
