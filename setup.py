from setuptools import setup, find_packages

setup(
    name="iedit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "boto3",
        "rich",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "iedit=iedit.cli:main",
        ],
    },
    author="iedit Team",
    author_email="info@iedit.com",
    description="A CLI tool for editing LaTeX files to improve form, syntax, and grammar using AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iedit/iedit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)