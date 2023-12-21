# coding: utf-8

"""
    NIUM Platform

    NIUM Platform

    Contact: experience@nium.com
    Do not edit the class manually.
"""  # noqa: E501


from setuptools import setup, find_packages  # noqa: H301

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "LONG_DESCRIPTION.rst").read_text()

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "nium"
VERSION = "1.0.0"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "urllib3 >= 1.25.3, < 2.1.0",
    "python-dateutil",
    "pydantic >= 1.10.5, < 2",
    "aenum"
]

setup(
    name=NAME,
    version=VERSION,
    description="NIUM Platform",
    author="NIUM Platform",
    author_email="experience@nium.com",
    url="",
    keywords=["NIUM Platform"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="Copyright (c) 2023 NIUM",
    long_description_content_type='text/x-rst',
    long_description=long_description,
  # noqa: E501
    package_data={"nium": ["py.typed"]},
)
