from setuptools import setup, find_packages

setup(
    name='maskingPackage',
    version='1.0.12',
    packages=find_packages(),
    install_requires=[
        'pandas',  # Add any dependencies here
        'cryptography'
    ],
)
