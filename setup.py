#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    path = os.path.join(package, "__init__.py")
    init_py = open(path, "r", encoding="utf8").read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_long_description():
    """
    Return the README.
    """
    return open("README.md", "r", encoding="utf8").read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


env_marker_cpython = (
    "sys_platform != 'win32'"
    " and (sys_platform != 'cygwin'"
    " and platform_python_implementation != 'PyPy')"
)

env_marker_win = "sys_platform == 'win32'"
env_marker_below_38 = "python_version < '3.8'"


setup(
    name="ai_commits",
    version=get_version("src"),
    url="https://github.com/Nneji123/aicommit",
    license="MIT",
    description="An AI-powered git commit message generator!",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Ifeanyi Nneji",
    author_email="ifeanyinneji777@gmail.com",
    packages=get_packages("aicommit"),
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=[
        "inquirer>=3.1.2",
        "openai>=0.26.1",
        "python-dotenv>=0.21.1",
        
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Code Generators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points="""
    [console_scripts]
    aicommit=src.aicommit:main
    """,
    project_urls={
        "Funding": "https://github.com/sponsors/Nneji123",
        "Source": "https://github.com/Nneji123/aicommit",
    },
)
