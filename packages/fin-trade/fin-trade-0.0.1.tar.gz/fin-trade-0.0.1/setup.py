from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Python-Finance'
LONG_DESCRIPTION = 'Powerful toolkit for analyzing and visualizing financial time-series data'

# Setting up
setup(
    name="fin-trade",
    version=VERSION,
    author="Poonam Deshmukh",
    author_email="poonamdeshmukh616@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'finance', 'algorithmic trading', 'technical indicators', 'poonam'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)