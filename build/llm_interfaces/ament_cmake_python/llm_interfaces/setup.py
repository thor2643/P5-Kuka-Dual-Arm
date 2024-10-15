from setuptools import find_packages
from setuptools import setup

setup(
    name='llm_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('llm_interfaces', 'llm_interfaces.*')),
)
