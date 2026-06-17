"""
Setup.py - Project configuration
"""
from setuptools import setup, find_packages

setup(
    name="bora-prorracha",
    version="1.0.0",
    description="Sports Space Booking System - Python Implementation",
    author="Development Team",
    author_email="dev@boraprorracha.com",
    url="https://github.com/example/bora-prorracha",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pytest>=7.4.3",
        "pytest-cov>=4.1.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    entry_points={
        "console_scripts": [
            "bora-proracha=main:main",
        ],
    },
)
