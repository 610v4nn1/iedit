from setuptools import setup, find_packages

setup(
    name='iedit',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'iedit = iedit:cli',
        ],
    },
)