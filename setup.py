from distutils.core import setup

import setuptools

setup(
    name='github-changelog-generator',
    version='0.0.1',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['github-changelog-generator=generator.cli:main'],
    },
    long_description=open('README.md').read(),
    install_requires=[
        'requests',
        'PyYAML'
    ],
)
