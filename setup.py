from setuptools import setup, find_packages

setup(
    name="iedit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "boto3",
        "botocore",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "iedit=iedit.cli:main",
        ],
    },
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool for editing LaTeX files to improve their form, syntax, and grammar using AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/iedit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
