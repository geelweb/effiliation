#!/usr/bin/env python
# -*- coding: utf8 -*-

from setuptools import setup, find_packages
import effiliation

setup(
    name = "Effiliation",
    version = effiliation.__version__,
    packages = find_packages(),
    author = "Guillaume Luchet",
    author_email = "guillaume@geelweb.org",
    description = "Client for the Effiliation API",
    license = "MIT License",
    keywords = "Effiliation Client affiliation",
    platforms = "ALL"
)

