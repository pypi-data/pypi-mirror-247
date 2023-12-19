# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     setup.py
   Description :
   Author :       yangzhixiang
   date：          2020/9/25
-------------------------------------------------
"""

import re

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
with open("clickpaas_toolkit/__init__.py", 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)
setup(
    name="clickpaas_toolkit",
    version=version,
    url="http://gitlab.autotest.clickpaas.tech/qa/clickpaas-toolkit",
    license="MIT",
    author="yangzhixiang",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=[
        "simplejson==3.16.0",
        "python-json-logger==0.1.9",
        "requests==2.28.0",
        "pymongo==3.6.1",
        "pymysql==0.9.1",
        "redis==2.10.6",
        "pycryptodomex==3.12.0",
    ],
    description="API Test Framework Toolkit",
    long_description=open("README.md", 'r', encoding='utf-8').read(),
)
