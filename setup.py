from setuptools import setup
from textual_filedrop import __version__ as VERSION

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as file:
    requires = [line.strip() for line in file.readlines()]

DESCRIPTION = (
    "FileDrop widget for Textual, easily drag and drop files into your terminal apps."
)

setup(
    name="textual-filedrop",
    version=VERSION,
    url="https://github.com/agmmnn/textual-filedrop",
    project_urls={
        "Changelog": "https://github.com/agmmnn/textual-filedrop/releases",
        "Source": "https://github.com/agmmnn/textual-filedrop",
    },
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="agmmnn",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    packages=["textual_filedrop"],
    install_requires=requires,
    include_package_data=True,
    package_data={"textual_filedrop": ["textual_filedrop/*"]},
    python_requires=">=3.7",
)
