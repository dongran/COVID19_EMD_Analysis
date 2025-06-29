#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="covid19-emd-analysis",
    version="1.0.0",
    author="randong",
    author_email="randong@example.com",
    description="COVID-19 EMD Analysis Tool - Epidemic transmission data analysis based on Empirical Mode Decomposition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/COVID19_EMD_Analysis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta", 
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": ["black", "flake8"],
        "docs": ["sphinx", "sphinx-rtd-theme"],
    },
    entry_points={
        "console_scripts": [
            "covid19-emd=examples.covid19_emd_analysis_example:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.csv"],
    },
    keywords="covid19, emd, analysis, epidemiology, time-series, signal-processing",
) 