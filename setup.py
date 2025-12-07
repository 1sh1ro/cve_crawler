#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cve-scraper",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A CVE vulnerability information scraper based on NVD official API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cve-scraper",
    py_modules=["cve_scraper"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cve-scraper=cve_scraper:main",
        ],
    },
    keywords="cve nvd security vulnerability scraper api",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/cve-scraper/issues",
        "Source": "https://github.com/yourusername/cve-scraper",
        "Documentation": "https://github.com/yourusername/cve-scraper#readme",
    },
)
