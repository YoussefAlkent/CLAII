from setuptools import setup, find_packages

setup(
    name="claai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "rich",
        "langchain-core",
        "langchain-openai",
        "langchain-ollama"
    ],
    entry_points={
        "console_scripts": [
            "claai=claai.cli:app",  # CLI entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
