#!/usr/bin/env python

import os
import sys


from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

packages = [
    'housenum-be-r-parser',
]

requires = [
    'nose',
    'coverage',
]

setup(
    name='housenum-be-r-parser',
    version='',
    description='',
    long_description=README,
    author='Onroerend Erfgoed',
    author_email='ict@onroerenderfgoed.be',
    url='http://github.com/onroerenderfgoed/housenum-be-r-parser',
    packages=find_packages(),
    package_data={'': ['LICENSE']},
    package_dir={'housenum-be-r-parser': 'housenum-be-r-parser'},
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tox'
)
