from os import getenv

extensions = ['sphinx_md']

# Configure path for repo files
# Environment variables are based on GitHub workflow defaults

sphinx_md_useGitHubURL = True
baseBranch = "devel"
commitSHA = getenv('GITHUB_SHA')
githubBaseURL = 'https://github.com/' + (getenv('GITHUB_REPOSITORY') or 'intel/pmem-csi') + '/'
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
