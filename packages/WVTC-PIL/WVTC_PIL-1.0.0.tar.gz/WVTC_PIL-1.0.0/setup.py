# -*- coding:utf-8 -*-
# @Author: Haoran Zhang
# @Time: 2023-11-10 14:59
# @File: setup.py
from setuptools import find_packages
from setuptools import setup

MAJOR = 1
MINOR = 0
PATCH = 0
VERSION = f"{MAJOR}.{MINOR}.{PATCH}"


def get_install_requires():
    reqs = [
            'requests>=2.0.0',
            'toml>=0.10',
            'numpy>=1.9.2'
            ]
    return reqs


setup(
    name='WVTC_PIL',
    version=VERSION,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.7",
    url='https://github.com/ENGR13200/tool',
    license='MIT',
    author='Null',
    author_email='251061929@qq.com',
    long_description=open('README.md', encoding="utf-8").read(),
    install_requires=get_install_requires(),
    package_data={'': ['*.csv', '*.txt', '.toml']},
)
