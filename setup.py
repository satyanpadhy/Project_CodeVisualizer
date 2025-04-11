from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="codebase-analyzer",
    version="0.1.0",
    author="Project Como Team",
    description="A tool for analyzing and visualizing code dependencies using Ollama",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/project-como/codebase-analyzer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            line.strip()
            for line in open("requirements-dev.txt", encoding="utf-8")
            if line.strip() and not line.startswith("#")
        ]
    },
    entry_points={
        "console_scripts": [
            "codebase-analyzer=codebase_analyzer.cli:main",
        ],
    },
)