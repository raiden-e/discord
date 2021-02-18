import json

import config
from github import Github, InputFileContent

gist_id = config.GIST_ID
token = config.GIST_TOKEN

gist = Github(token).get_gist(gist_id)


def load(gist_name):
    x = gist.files[gist_name].content
    return json.loads(x)


def update(filename: str, content=None, description: str = "", default=None):
    if not isinstance(filename, str):
        raise ValueError("filename has to be specified and be str")
    if not content:
        raise ValueError("No content")

    raw = json.dumps(content, indent=2, default=default)
    gist.edit(
        description=description,
        files={filename: InputFileContent(raw)})
