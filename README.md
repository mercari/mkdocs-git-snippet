# mkdocs-git-snippet [![Test][test-badge]][test] [![Code style: black][black-badge]][black]

<!-- badge links -->
[test-badge]: https://github.com/mercari/mkdocs-git-snippet/workflows/Test/badge.svg
[test]: https://github.com/mercari/mkdocs-git-snippet/actions?query=workflow%3ATest
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black]: https://github.com/psf/black

Mkdocs Plugin for snippet from git repository.

## Installation

```shell
pip install mkdocs-git-snippet
```

## Configuration

Enable the plugin in your mkdocs.yml.

```markdown
plugins:
  - git-snippet
```

If the folder name that contain your documentation source files is not default `docs`, you need specify it with `base_path` option.

```markdown
plugins:
  - git-snippet:
        base_path: docs
```

By default, this plugin works for all pages. You can enable only for the specific page by setting `all_pages` option to false.

```markdown
plugins:
  - git-snippet:
      all_pages: false
```

When `all_pages` is false, this plugin only works for the page that added `git-snippet: enable`.

```markdown
<!-- git-snippet: enable -->

# Your document
....
```

### Acessing Private Repositories

To add a snippet from a private repository set the `GITHUB_TOKEN` environment variable while building mkdocs documentation.

## Usage

### All files from default branch

```
{{ gitsnippet('mkdocs/mkdocs', 'docs/user-guide/plugins.md') }}
```

It works for non markdown file too. The snippet format is raw text.
Please format it if needed.

````
```python
{{ gitsnippet('mkdocs/mkdocs', 'mkdocs/config/base.py') }}
```
````

### All files from specific branch/tag/commit

````
```python
{ gitsnippet('mkdocs/mkdocs', 'mkdocs/config/base.py', '1.1')
```
````

````
```python
{{ gitsnippet('mkdocs/mkdocs', 'mkdocs/config/base.py', '520314fed933aed8de62b08dd7fc6e25c0ff482b') }}
```
````

### Snippet a section

For markdown file, it is possible to specify a section.
```
{{ gitsnippet('mkdocs/mkdocs', 'docs/user-guide/plugins.md', section='## Using Plugins') }}
```
or
```
{{ gitsnippet('mkdocs/mkdocs', 'docs/user-guide/plugins.md', 'master', '## Using Plugins') }}
```

### Insert indent

You can insert indent to snippet using `indent`.
`indent` has an argument `width`, which means the number of space to indent by. The default is 4.
See more details of `indent` [here](https://jinja.palletsprojects.com/en/master/templates/#indent).

````
??? example "Plugin.md"

    {{ gitsnippet('mkdocs/mkdocs', 'docs/user-guide/plugins.md') | indent }}

    !!! note

        ```python
        {{ gitsnippet('mkdocs/mkdocs', 'mkdocs/config/base.py) | indent(width=8) }}
        ```
````

## Contribution

Please read the CLA carefully before submitting your contribution to Mercari.
Under any circumstances, by submitting your contribution, you are deemed to accept and agree to be bound by the terms and conditions of the CLA.

https://www.mercari.com/cla/

## License

Copyright 2021 Mercari, Inc.

Licensed under the MIT License.
