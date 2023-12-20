from setuptools import setup, find_packages

setup(
    name='dasty_api',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'certifi==2023.11.17',
        'charset-normalizer==3.3.2',
        'idna==3.6',
        'PyYAML==6.0.1',
        'requests==2.31.0',
        'urllib3==2.1.0'
    ],
)
