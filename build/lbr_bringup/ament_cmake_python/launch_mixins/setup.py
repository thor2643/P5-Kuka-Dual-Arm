from setuptools import find_packages
from setuptools import setup

setup(
    name='launch_mixins',
    version='2.0.0',
    packages=find_packages(
        include=('launch_mixins', 'launch_mixins.*')),
)
