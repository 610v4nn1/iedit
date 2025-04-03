from setuptools import setup, find_packages

setup(
    name="iedit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "boto3",  # For AWS Bedrock integration
        "click",  # For CLI interface
        "PyYAML",  # For configuration handling
    ],
    entry_points={
        "console_scripts": [
            "iedit=iedit.cli:main",
        ],
    },
    author="Author",
    author_email="author@example.com",
    description="A CLI tool for editing LaTeX files using AI to improve form, syntax and grammar",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/author/iedit",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)