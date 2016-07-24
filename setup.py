#!/usr/bin/env python
import re
import os

from setuptools import setup

module = "lessql"

with open("README.rst") as fp:
    long_desc = fp.read()

with open("{}/__init__.py".format(module)) as fp:
    version = re.search('__version__\s+=\s+"([^"]+)', fp.read()).group(1)

if __name__ == "__main__":
    setup(
        name="LesSQL",
        version=version,
        description="Write less SQL and become more productive",
        long_description=long_desc,
        license="MIT",
        author="Andreas Runfalk",
        author_email="andreas@runfalk.se",
        url="https://www.github.com/runfalk/lessql",
        py_modules=[module],
        install_requires=[],
        extras_require={
            "dev": [
                "pytest",
                "pytest-cov",
            ],
            # Backports
            ":python_version < '3.3'": [
                "chainmap",
            ],
            ":python_version < '3.4'": [
                "enum34",
            ],
        },
        classifiers=(
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Topic :: Utilities",
        )
    )
