import os
import re
import urllib.request
from pathlib import Path

import parse
from github import Repository


def skip_page(markdown: str) -> bool:
    template = "git-snippet: {action:S}"
    result = parse.search(template, markdown)
    if result:
        if result["action"] == "enable":
            return False
    return True


def copy_markdown_images(root: str, file: str, repo: Repository, markdown: str) -> str:
    template = "![{name}]({path})"
    paths = [result["path"] for result in parse.findall(template, markdown)]
    parent = Path(file).parent
    for path in paths:
        if path.startswith("http"):
            continue
        img_path = Path(parent / path).resolve().relative_to(Path(".").resolve())

        img = repo.get_contents(str(img_path))
        destination = os.path.realpath(f"{root}/gen_/{img_path}")
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        urllib.request.urlretrieve(img.download_url, destination)

        markdown = markdown.replace(path, f"gen_/{img_path}")
    return markdown


def get_markdown_section(content: str, section: str) -> str:
    section_pattern = re.compile("^#+ ")
    match = section_pattern.search(section)
    if not match:
        raise ValueError(f"Invalid section name: {section}")
    section_level = match.span()[1] - 1
    target = re.compile("^" + section + "$", re.MULTILINE)
    start = target.search(content)
    if not start:
        raise ValueError(f"Not found: {section}")
    start_index = start.span()[1]

    end_target = re.compile("^#{1," + str(section_level) + "} ", re.MULTILINE)
    end = end_target.search(content[start_index:])
    if end:
        end_index = end.span()[0]
        content = content[start_index : end_index + start_index]
    else:
        content = content[start_index:]
    return content
