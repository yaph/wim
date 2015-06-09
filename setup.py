#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with io.open('README.rst') as f:
    readme = f.read()

with io.open('HISTORY.rst') as f:
    history = f.read().replace('.. :changelog:', '')

with io.open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='wim',
    version='0.1.1',
    description='wim is a command line tool to create Web images.',
    long_description=readme + '\n\n' + history,
    author='Ramiro Gómez',
    author_email='code@ramiro.org',
    url='https://github.com/yaph/wim',
    packages=['wim',],
    package_dir={'wim': 'wim'},
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords='wim',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'wim = wim.wim:main'
        ]
    }
)
