#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', "Rich", "PyYAML"]

test_requirements = [ ]

setup(
    author="Jaideep Sundaram",
    author_email='jai.python3@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A package for profiling the files in a data directory",
    entry_points={
        'console_scripts': [
            'profile-data-directory=profile_data_directory.profile_data_directory:main',
            'survey_dataset_directory=profile_data_directory.survey_dataset_directory:main',
            'copy_dataset_files=profile_data_directory.copy_dataset_files:main',
            'find-last-directory=profile_data_directory.find_last_directory:main',
            'find-last-file=profile_data_directory.find_last_file:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='profile_data_directory',
    name='profile_data_directory',
    packages=find_packages(include=['profile_data_directory', 'profile_data_directory.*']),
    package_data={"profile_data_directory": ["conf/config.yaml"]},
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jai-python3/profile-data-directory',
    version='0.2.1',
    zip_safe=False,
)
