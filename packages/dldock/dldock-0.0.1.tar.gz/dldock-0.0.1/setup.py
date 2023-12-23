#!/usr/bin/env python3
from setuptools import setup
from pathlib import Path

description = (Path(__file__).resolve().parent / "README.md").read_text()
setup(name='dldock',
      version='0.0.1',
      description='Shared Library Handler Based on Ctypes',
      author='Sean West',
      long_description=description,
      long_description_content_type='text/markdown',
      keywords="shared library handler",
      license='MIT',
      packages = ['dldock'],
      python_requires='>=3.8',
      include_package_data=True)