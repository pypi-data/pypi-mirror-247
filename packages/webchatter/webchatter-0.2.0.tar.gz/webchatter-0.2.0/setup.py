#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
VERSION = '0.2.0'

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', 'tqdm>=4.60', 'chattool>=3.0.0']

setup(
    author="Rex Wang",
    author_email='1073853456@qq.com',
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Wrapper of the web server of ChatGPT",
    install_requires=requirements,
    license="MIT license",
    # long_description=readme,
    include_package_data=True,
    keywords='webchatter',
    name='webchatter',
    packages=find_packages(include=['webchatter', 'webchatter.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/RexWzh/webchatter',
    version=VERSION,
    zip_safe=False,
)
