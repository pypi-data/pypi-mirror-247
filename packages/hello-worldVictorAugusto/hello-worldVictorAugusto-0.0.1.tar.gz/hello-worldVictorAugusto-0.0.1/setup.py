# setup.py
from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name='hello-worldVictorAugusto',
    version='0.0.1',
    license='MIT License',
    author='Victor Augusto',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='victoraugustodocarmo32@gmail.com',
    keywords='hello world',
    description='Uma biblioteca simples que exibe Hello, World!',
    packages=find_packages(),
    install_requires=[],
)
