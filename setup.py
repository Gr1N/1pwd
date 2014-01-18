# -*- coding: utf-8 -*-

import os

from setuptools import setup
from setuptools import find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='onepyssword',
    version='0.2',
    description='A command line interface for 1Password',
    long_description=read('README.md') +
                     read('HISTORY.md') +
                     read('LICENSE'),
    classifiers=[
        'Programming Language :: Python',
    ],
    author='Nikita Grishko',
    author_email='grin.minsk@gmail.com',
    url='https://github.com/Gr1N/1pwd',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'pbkdf2-ctypes==0.99.3',
        'pycrypto==2.6.1',
        'xerox==0.3.1',
    ],
    extras_require={
        'test': [
            'tox',
            'pytest',
        ],
        'development': [
            'zest.releaser',
            'check-manifest',
        ],
    },
    entry_points="""
    """,
    include_package_data=True,
    zip_safe=False,
    scripts=[
        'bin/1pwd',
    ],
)
