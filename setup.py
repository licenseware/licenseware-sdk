from setuptools import setup, find_packages
import re


# Distribute py wheels
# python3 setup.py bdist_wheel sdist
# twine check dist/*
# cd dist
# twine upload *


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    REQUIREMENTS = fh.readlines()
    
    
    
VERSION = 'UNKNOWN'

with open("CHANGELOG.md", "r") as fh:
    changelog = fh.readlines()

if len(changelog) > 2:    
    raw_version = changelog[2]
    version_match = re.search(r'### \[(\d+\.\d+\.\d+)\]', raw_version)
    if version_match:
        VERSION = version_match.group(1)




setup(
    name="licenseware",
    version=VERSION,
    description="Common utilities for licenseware.",
    url="https://github.com/licenseware/licenseware-sdk",
    author="licenseware",
    author_email="contact@licenseware.io",
    license='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=REQUIREMENTS,
    package_dir={"": "src"},
    packages=find_packages(
        where="src",
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    )
)
