import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphinx-md",
    version="0.0.4",
    author="Kevin Putnam",
    author_email="kevin.putnam@intel.com",
    description="Sphinx extension to use with Recommonmark or MystParser to fix links to rst from md, links to md from rst, and links to embedded files and dirs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/intelkevinputnam/sphinx-md",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['recommonmark','sphinx-markdown-tables','bs4'],
)
