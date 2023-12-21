# TheFunPackage - setup.py

''' This is the 'setup.py' file. '''

'''
Copyright 2023 Aniketh Chavare

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
from setuptools import setup, find_packages

# README.md
with open("README.md") as readme_file:
    README = readme_file.read()

# Setup Arguments
setup_args = dict (
    name = "TheFunPackage",
    version = "1.0.6",
    description = "This package is only meant for fun and to entertain you!",
    long_description = README,
    long_description_content_type = "text/markdown",
    license = "Apache License 2.0",
    packages = find_packages(),
    include_package_data = True,
    author = "Aniketh Chavare",
    author_email = "anikethchavare@outlook.com",
    project_urls = {
        "Homepage": "https://pypi.org/project/TheFunPackage",
        "Repository": "https://github.com/anikethchavare/TheFunPackage",
        "Documentation": "https://anikethchavare.gitbook.io/thefunpackage",
        "Download": "https://github.com/anikethchavare/TheFunPackage/releases",
        "Changelog": "https://github.com/anikethchavare/TheFunPackage/blob/main/CHANGELOG.md",
        "Issues": "https://github.com/anikethchavare/TheFunPackage/issues"
    },
    install_requires = [
        "PySyst",
        "colorama",
        "requests",
        "pyjokes",
        "randfacts"
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development"
    ]
)

# Running the Setup File
if __name__ == "__main__":
    setup(**setup_args)