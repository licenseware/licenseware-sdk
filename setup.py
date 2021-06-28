from setuptools import setup, find_packages
import re


# Distribute py wheels
# python3 setup.py bdist_wheel sdist
# twine check dist/*
# cd dist
# twine upload *


with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.readlines()
    
    
    
VERSION = 'UNKNOWN'

with open("CHANGELOG.md", "r") as f:
    changelog = f.read()

if '# Changelog' in changelog:    
    version_match = re.match(f'#\s+Changelog\n+#+\s*\[((\d+\.\d+\.\d+))\]\(', changelog)
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
