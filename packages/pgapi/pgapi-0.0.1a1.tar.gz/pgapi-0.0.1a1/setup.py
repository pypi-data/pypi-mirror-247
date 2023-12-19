from setuptools import setup, find_packages
import io
import os

VERSION = "0.0.1a1"


def get_long_description():
    with io.open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="pgapi",
    description="CLI tool and Python library for manipulating Postgres databases",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Florents Tselai",
    author_email="florents@tselai.com",
    version=VERSION,
    license="Apache License, Version 2.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"pgapi": ["py.typed"]},
    install_requires=[
        "psycopg[binary,pool]",
        "sqlite-fts4",
        "click",
        "click-default-group>=1.2.3",
        "tabulate",
        "python-dateutil",
        "pluggy",
    ],
    extras_require={
        "test": ["pytest", "black", "hypothesis", "cogapp"],
        "docs": [
            "furo",
            "sphinx-autobuild",
            "codespell",
            "sphinx-copybutton",
            "beanbag-docutils>=2.0",
            "pygments-csv-lexer",
        ],
        "mypy": [
            "mypy",
            "types-click",
            "types-tabulate",
            "types-python-dateutil",
            "types-pluggy",
            "data-science-types",
        ],
        "flake8": ["flake8"],
        "tui": ["trogon"],
    },
    entry_points="""
        [console_scripts]
        pgapi=pgapi.cli:cli
    """,
    url="https://github.com/Florents-Tselai/pgAPI",
    project_urls={
        "Documentation": "https://pgAPI.tselai.com/en/stable/",
        "Changelog": "https://pgAPI.tselai.com/en/stable/changelog.html",
        "Source code": "https://github.com/Florents-Tselai/pgAPI",
        "Issues": "https://github.com/Florents-Tselai/pgAPI/issues",
        "CI": "https://github.com/Florents-Tselai/pgAPI/actions",
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Database",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    # Needed to bundle py.typed so mypy can see it:
    zip_safe=False,
)
