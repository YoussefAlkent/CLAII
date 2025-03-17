from setuptools import setup, find_packages

setup(
    name="claii-ai",
    version="0.1.0",
    author="YoussefAlkent",
    author_email="youssefalkent@gmail.com",
    description="Command Line Artificial Intelligence Interface, an AI for your CLI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YoussefAlkent/CLAII",
    packages=find_packages(),
    install_requires=[
        "typer",
        "rich",
        "pytest",
        "pytest-mock",
        "langchain-core",
        "langchain-openai",
        "langchain-ollama",
        "langchain-deepseek",
        "langchain-anthropic",
        "langchain-mistralai",
        "langchain-google-genai"

    ],
    entry_points={
        "console_scripts": [
            "claii=claii.app:app",  # CLI entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
