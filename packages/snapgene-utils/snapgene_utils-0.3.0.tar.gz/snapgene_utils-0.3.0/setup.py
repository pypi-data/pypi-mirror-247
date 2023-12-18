"""
setup.py
install snapgene_utils by pip
"""
from setuptools import find_packages, setup

setup(
    name="snapgene_utils",
    version="0.3.0",
    author="poeticpete",
    maintainer="petertao",
    description="Convert Snapgene *.dna files dict/json/biopython.",
    long_description=open("README.rst").read(),
    license="MIT",
    keywords="DNA sequence design format converter",
    packages=find_packages(),
    install_requires=["biopython", "xmltodict", "html2text"],
)
