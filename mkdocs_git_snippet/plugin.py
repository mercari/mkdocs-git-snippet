import os

import mkdocs
from mkdocs.plugins import BasePlugin
from jinja2 import Template
from github import Auth, Github, GithubObject

from mkdocs_git_snippet.util import (
    skip_page,
    copy_markdown_images,
    get_markdown_section,
)


class GitSnippetPlugin(BasePlugin):
    config_scheme = (
        ("base_path", mkdocs.config.config_options.Type(str, default="docs")),
        ("all_pages", mkdocs.config.config_options.Type(bool, default=True)),
    )
    page = None

    def _git_snippet(self, repository: str, file: str, ref: str, section: str) -> str:
        g = Github(auth=Auth.Token(os.getenv("GITHUB_TOKEN")))
        repo = g.get_repo(repository)
        f = repo.get_contents(file, ref=ref)
        content = f.decoded_content.decode("utf-8")
        if section:
            content = get_markdown_section(content, section)

        root = f"{self.config['base_path']}/{self.page.url}"
        content = copy_markdown_images(root, file, repo, content)
        return content

    def gitsnippet(
        self,
        repository: str,
        file: str,
        ref: str = GithubObject.NotSet,
        section: str = None,
    ) -> str:
        return self._git_snippet(repository, file, ref, section)

    def on_page_markdown(self, markdown, page, config, **kwargs):
        if not self.config["all_pages"] and skip_page(markdown):
            return markdown
        self.page = page
        md_template = Template(markdown)
        return md_template.render(gitsnippet=self.gitsnippet)
