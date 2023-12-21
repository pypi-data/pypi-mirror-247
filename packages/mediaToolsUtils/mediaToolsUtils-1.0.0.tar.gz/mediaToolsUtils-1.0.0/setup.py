from __future__ import print_function
from setuptools import setup, find_packages
import mediaToolsUtils

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="mediaToolsUtils",
    version=mediaToolsUtils.__version__,
    author="nicknice",
    # author_email="kjxyzhaobo@163.com",
    description="free python media tools utils written by python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    # url="https://github.com/MemoryD/mxgames",
    packages=find_packages(),
    install_requires=[
        # "pygame <= 1.9.5",
        ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
