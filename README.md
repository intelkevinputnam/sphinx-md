# Sphinx Markdown Extension

This extension fixes or improves how Sphinx handles links related to Markdown
when it generates the HTML site. It assumes you are using the `recommonmark`
extension. It's a good idea to use `sphinx_markdown_tables` as well.

**Contents**

- [What it does](#what-it-does)
- [How to use it](#how-to-use-it)

## What it does

1. Markdown files: Converts references to Markdown files that include anchors.
   ``` md
   [configuration options](autotest.md#configuration-options)
   ```
2. reST files: Fixes explicit links to Markdown files.
   ``` rst
   `Google Cloud Engine <gce.md>`__
   ```
3. Markdown files: Fixes references to reST files.
   ``` md
   [Application examples](examples/readme.rst)
   ```
4. Markdown files: Fixes links to files and directories within the GitHub repo.
   ``` md
   [Makefile](/Makefile)
   [deploy/kustomize](/deploy/kustomize)
   ```
   Links to files can be fixed one of two ways, which can be set in the
   [conf.py](/conf.py).

   ``` python
   baseBranch = "devel"
   useGitHubURL = True
   commitSHA = getenv('GITHUB_SHA')
   githubBaseURL = "https://github.com/intelkevinputnam/pmem-csi/"
   ```

   If ``useGitHubURL`` is set to True, it will try to create links based on
   your ``githubBaseURL`` and the SHA for the commit to the GitHub repo
   determined by the GitHub workflow on merge). If there is no SHA available,
   it will use the value of ``baseBranch``.

   If ``useGitHubURL`` is set to False, it will copy the files to the HTML
   output directory and provide links to that location.

   NOTE: Links to files and directories should use absolute paths relative to
   the repo (see Makefile and deploy/kustomize above). This will work both for
   the Sphinx build and when viewing in the GitHub repo.

   Links to directories are always converted to links to the GitHub repository.

## How to use it

1. Install the sphinx_md extension:

   ``` bash
   pip3 install sphinx_md
   ```

2. Add `sphinx_md` to the extensions in your `conf.py`:

   ``` python
   extensions = ['sphinx_md', ...]
   ```

3. If you want to use GitHub commit links, add the entire code snippet to
   your `conf.py`:

   ``` python
   from os import getenv

   sphinx_md_useGitHubURL = True
   baseBranch = "devel"
   commitSHA = getenv('GITHUB_SHA')
   githubBaseURL = 'https://github.com/' + (getenv('GITHUB_REPOSITORY') or '<your_group/your_project>') + '/'
   githubFileURL = githubBaseURL + "blob/"
   githubDirURL = githubBaseURL + "tree/"
   if commitSHA:
       githubFileURL = githubFileURL + commitSHA + "/"
       githubDirURL = githubDirURL + commitSHA + "/"
   else:
       githubFileURL = githubFileURL + baseBranch + "/"
       githubDirURL = githubDirURL + baseBranch + "/"
   sphinx_md_githubFileURL = githubFileURL
   sphinx_md_githubDirURL = githubDirURL
   ```