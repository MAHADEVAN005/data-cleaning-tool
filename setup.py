from setuptools import setup, find_packages

setup(
    name="data-cleaner-mahadevan",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["pandas"],
    entry_points={
        "console_scripts": [
            "datacleaner=cli:main",
        ]
    }
)
