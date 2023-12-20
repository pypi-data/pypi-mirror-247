#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', "colorama"]

test_requirements = [ ]

setup(
    author="Jaideep Sundaram",
    author_email='jai.python3@gmail.com',
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
    description="Software for generating Umlet class diagrams of a Python code base",
    entry_points={
        'console_scripts': [
            'umlet-utils-python-api-to-umlet-class-diagram=umlet_utils.python_api_to_umlet:main',
            'umlet-utils-survey-python-codebase=umlet_utils.survey_python_code_base:main',
            'umlet-utils-yaml-to-use-case=umlet_utils.yaml_to_umlet_use_case:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='umlet_utils',
    name='umlet_utils',
    packages=find_packages(include=['umlet_utils', 'umlet_utils.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jai-python3/umlet-utils',
    version='0.1.0',
    zip_safe=False,
)
