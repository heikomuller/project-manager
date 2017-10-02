#! /usr/bin/env python

from setuptools import setup

setup(
    name='prjrepo',
    version='0.1.0',
    description='Library to manage and execute workflow commands (scripts) as part of a data science project',
    keywords='data science project manager ',
    author='Heiko Mueller',
    author_email='heiko.muller@gmail.com',
    url='https://github.com/heikomuller/experiment-repository',
    license='GPLv3',
    packages=['prjrepo'],
    package_data={'': ['LICENSE']},
    install_requires=['pyyaml']
)
