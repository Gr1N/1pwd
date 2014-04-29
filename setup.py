# -*- coding: utf-8 -*-

import os

from setuptools import setup
from setuptools import find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = """{0}

{1}
""".format(read('README.rst'), read('HISTORY.rst'))


setup(
    name='onepyssword',
    version='0.3.2',
    description='A command line interface for 1Password',
    long_description=long_description,
    classifiers=(
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
    author='Nikita Grishko',
    author_email='grin.minsk@gmail.com',
    url='http://gr1n.github.io/1pwd/',
    license='MIT',
    packages=find_packages(),
    install_requires=(
        'setuptools',
        'pbkdf2-ctypes>=0.99.3',
        'pycrypto>=2.6.1',
        'copypaste>=0.2.0',
    ),
    extras_require={
        'test': (
            'tox',
            'pytest',
        ),
        'development': (
            'flake8',
            'zest.releaser',
            'check-manifest',
        ),
    },
    include_package_data=True,
    zip_safe=False,
    scripts=(
        'bin/1pwd',
    ),
)
