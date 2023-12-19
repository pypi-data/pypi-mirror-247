from setuptools import setup, find_packages

VERSION = "0.0.1"

DESCRIPTION = """
A programatical alternative to the visual chatbot builder provided by https://botnoi.ai . It can be used to build and train chatbots for various platforms such as Facebook Messenger and LINE.
"""

LONG_DESCRIPTION = """
Botnoi Dev Platform is a programatical alternative to the visual chatbot builder provided by https://botnoi.ai . It can be used to build and train chatbots for various platforms such as Facebook Messenger and LINE.

This official library provides a Python implementation of Botnoi Dev Platform's API in order to simplify the process of building chatbots. It also provides various data types related to chatbots such as 'Intent', 'ImageObject', 'DialogueObject' and lots of helper functions to work with them.

This suits best for developers who want to build chatbots programmatically or to automate the process of chatbot training when an action is performed by the users.
"""

# Setting up
setup(
    name="botnoi_dev_platform",
    version=VERSION,
    author="Jira Pit @ BOTNOI GROUP",
    author_email="<jira.p@botnoigroup.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=[],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)