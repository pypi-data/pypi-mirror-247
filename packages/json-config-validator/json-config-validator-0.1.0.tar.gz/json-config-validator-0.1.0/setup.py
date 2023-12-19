#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "jsonschema", "colorama"]

test_requirements = []

setup(
    author="Jaideep Sundaram",
    author_email="jai.python3@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Package for validation JSON configuration files",
    entry_points={
        "console_scripts": [
            "json-config-validator=json_config_validator.main:main",
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="json_config_validator",
    name="json-config-validator",
    packages=find_packages(
        include=["json_config_validator", "json_config_validator.*"]
    ),
    package_data={"json_config_validator": ["conf/config.yaml"]},
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jai-python3/json-config-validator",
    version="0.1.0",
    zip_safe=False,
)
