from setuptools import setup, find_packages

setup(
    name="iedit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.28.0",
        "click>=8.0.0",
        "PyYAML>=6.0",
    ],
    entry_points={
        'console_scripts': [
            'iedit=iedit.cli:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool for editing LaTeX files using AI via Amazon Bedrock",
    long_description=open("definition.md").read(),
    long_description_content_type="text/markdown",
    keywords="latex, editing, ai, amazon-bedrock",
    python_requires=">=3.8",
)