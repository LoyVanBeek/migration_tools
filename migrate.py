#!/user/bin/python

from pygithub3 import Github

gh = Github(login=USERNAME, password=PASSWORD)

repo = gh.repos.create(dict(name=REPO_NAME, description=DESCRIPTION, gitignore_template='python', auto_init=True), in_org='tue-robotics-lab')

print repo
