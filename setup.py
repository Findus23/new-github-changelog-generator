from distutils.core import setup

import setuptools

setup(
    name='github-changelog-generator',
    version='0.0.1',
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['github-changelog-generator=generator.cli:main'],
    }
    # license='Creative Commons Attribution-Noncommercial-Share Alike license',
    # long_description=open('README.md').read(),
)