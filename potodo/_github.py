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

    issues: list = []
    next = "https://api.github.com/repos/" + get_repo_name() + "/issues?state=open"
    while next:
        resp = requests.get(next)
        issues += issues
        next = resp.links.get("next", {}).get("url")

    reservations = {}

    for issue in issues:
        # Maybe find a better way for not using python 3.8 ?
        if re.search(r'\w*/\w*\.po', issue['title']):
            yes = re.search(r'\w*/\w*\.po', issue['title'])
            reservations[yes.group()] = issue['user']['login']

    return reservations
