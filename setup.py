#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'grpcio==1.46.2',
    'reactivex==4.0.0',
    'protobuf==3.20.1'
]

test_requirements = [ ]

setup(
    author="Turning Data Into Products AS",
    author_email='Ariel Fischer',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Qapio Python Core contains all you need for communicationg with Qapio.",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='qapio_python_core',
    name='qapio_python_core',
    packages=find_packages(include=['qapio_python_core', 'qapio_python_core.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tdip/qapio_python_core',
    version='0.1.0',
    zip_safe=False,
)
