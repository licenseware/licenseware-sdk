from setuptools import setup, find_packages

#Distribute py wheels
#python3 setup.py bdist_wheel sdist
#twine check dist/*
#cd dist 
#twine upload *

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", 'r') as f:
	requirements = f.readlines()


setup(
	name="licenseware",
	version="0.0.3",
	description="Common utilities for licenseware.",
	url="https://github.com/licenseware/licenseware-sdk",
	author="licenseware",
	author_email="contact@licenseware.io",
	license='',
	long_description=long_description,
    long_description_content_type="text/markdown",
	install_requires=requirements,
	package_dir={"":"src"},
	packages=find_packages(
		where="src",
		exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
	)
)

