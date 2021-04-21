from setuptools import setup, find_packages

#Distribute py wheels
#python3 setup.py bdist_wheel sdist
#twine check dist/*
#cd dist 
#twine upload *

with open("README.md", "r") as fh:
    long_description = fh.read()

DEPENDENCIES = [
	"pandas", 
	"openpyxl",
	"flask", 
	"redis",
	"loguru",
	"requests",
	"pymongo",
	"marshmallow"
]



setup (
	name="lware",
	version="0.0.1",
	description="Common utilities for licenseware.",
	url="https://github.com/licenseware/lware-components",
	author="licenseware",
	author_email="contact@licenseware.io",
	license='',
	py_modules=["lware"],
	install_requires=DEPENDENCIES,
	packages=find_packages(exclude=("lware/tests",)),
	long_description=long_description,
    long_description_content_type="text/markdown",
	package_dir={"":"./src/lware"}
)