from setuptools import find_packages, setup

requires = ["prompt_toolkit==2.0.9", "awslogs"]
dev_requires = ["pytest", "pytest-sugar", "pytest-mock", "black"]

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="awslogs_watch",
    version="0.2.0",
    description="awslogs-watch is a CLI tool that makes it easy to use awslogs",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="deresmos",
    author_email="deresmos@gmail.com",
    url="https://github.com/deresmos/awslogs-watch",
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=False,
    keywords=["tools"],
    license="MIT License",
    install_requires=requires,
    extras_require={"develop": dev_requires},
    entry_points={
        "console_scripts": ["awslogs-watch = awslogs_watch.console:start_console"]
    },
)
