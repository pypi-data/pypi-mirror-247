from setuptools import setup, find_packages

VERSION = "0.0.8"

DESCRIPTION = """
A programatical alternative to the visual chatbot builder provided by https://botnoi.ai . 
It can be used to build and train chatbots for various platforms such as Facebook Messenger and LINE.
"""

LONG_DESCRIPTION = open("LONG_DESCRIPTION.md", "r", encoding="utf-8").read()

setup(
    name="botnoi_dev_platform",
    version=VERSION,
    author="Jira Pit @ BOTNOI GROUP",
    author_email="<jira.p@botnoigroup.com>",
    maintainer="Jira Pit @ BOTNOI GROUP",
    maintainer_email="<jira.p@botnoigroup.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(
        exclude=["test", "test.*"]
    ),
    install_requires=['requests'],
    keywords=["botnoi", "chatbot", "bot", "botnoi dev platform"],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)