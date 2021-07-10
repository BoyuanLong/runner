import setuptools
from setuptools import setup


setup(
    # Information
    name='runner',
    description='Runner for Hyperparameter Tuning',
    version='0.0.1',
    author='Boyuan Long',
    install_requires=[
        'colorlog',
    ],

    package_dir={'': './'},
    packages=setuptools.find_packages(where='./', exclude='runs'),
    include_package_data=True,

    python_requires='>=3.6',
)