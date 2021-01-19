import textwrap

import pytest
from mock import Mock, patch

from mkdocs_git_snippet.util import (
    copy_markdown_images,
    get_markdown_section,
    skip_page,
)


class TestSkipPage(object):
    def test_not_skip(self):
        assert not skip_page("<!-- git-snippet: enable -->")

    def test_skip(self):
        assert skip_page("# test")

    def test_skip_with_template(self):
        assert skip_page("<!-- git-snippet: comment -->")


class TestCopyMarkdownImages(object):
    img = Mock()
    img.download_url = "http://url/test"

    repo = Mock()
    repo.get_contents.return_value = img

    root = "test/root/"
    file = "local/test.md"

    @patch("os.makedirs")
    @patch("urllib.request.urlretrieve")
    def test_single_image(self, *_):
        markdown = textwrap.dedent(
            """
            # test
            This section has an image.
            ![img_name](original/img_path/img.png)
            """
        )
        result = copy_markdown_images(self.root, self.file, self.repo, markdown)
        expected = textwrap.dedent(
            """
            # test
            This section has an image.
            ![img_name](gen_/local/original/img_path/img.png)
            """
        )
        assert result == expected

    @patch("os.makedirs")
    @patch("urllib.request.urlretrieve")
    def test_multiple_images(self, *_):
        markdown = textwrap.dedent(
            """
            # test
            This section has an image.
            ![img_name](original/img_path/img.png)
            ## section2
            This section has an image too.
            ![img_name2](original2/img_path2/img2.png)
            """
        )
        result = copy_markdown_images(self.root, self.file, self.repo, markdown)
        expected = textwrap.dedent(
            """
            # test
            This section has an image.
            ![img_name](gen_/local/original/img_path/img.png)
            ## section2
            This section has an image too.
            ![img_name2](gen_/local/original2/img_path2/img2.png)
            """
        )
        assert result == expected

    @patch("os.makedirs")
    @patch("urllib.request.urlretrieve")
    def test_url_images(self, *_):
        markdown = textwrap.dedent(
            """
            # test
            This section has an image.
            ![img_name](http://original/img_path/img.png)
            ## section2
            This section has an image too.
            ![img_name2](https://original2/img_path2/img2.png)
            """
        )
        result = copy_markdown_images(self.root, self.file, self.repo, markdown)
        expected = markdown
        assert result == expected

    @patch("os.makedirs")
    @patch("urllib.request.urlretrieve")
    def test_no_image(self, *_):
        markdown = textwrap.dedent(
            """
            # test
            This section doesn't have an image.
            [link](this/is/not/image)
            """
        )
        result = copy_markdown_images(self.root, self.file, self.repo, markdown)
        expected = markdown
        assert result == expected


class TestCopyMarkdownSection(object):
    content = textwrap.dedent(
        """
        # Header 1-1
        ## Header 2
        This line is under Header 2
        # Header 1-2
        This line is under Header 1-2
        """
    )

    def test_h1(self):
        section = "# Header 1-1"
        result = get_markdown_section(self.content, section)
        expected = textwrap.dedent(
            """
            ## Header 2
            This line is under Header 2
            """
        )
        assert result == expected

    def test_h2(self):
        section = "## Header 2"
        result = get_markdown_section(self.content, section)
        expected = textwrap.dedent(
            """
            This line is under Header 2
            """
        )
        assert result == expected

    def test_invalid_section(self):
        section = "Invalid Section"
        with pytest.raises(ValueError):
            get_markdown_section(self.content, section)

    def test_section_not_found(self):
        section = "## Not Exist Header"
        with pytest.raises(ValueError):
            get_markdown_section(self.content, section)
