<p align="center">

<p align="center">
   <img width="50%" height="40%" src="https://tselai.com/data/babar-1.png" alt="Logo">
  </p>

  <h1 align="center">pgAPI</h1>
  <p align="center">
  <strong>CLI tool and Python library for manipulating Postgres databases</strong>
    <br> <br />
    <a href="#inspiration"><strong> Inspiration </strong></a> |
    <a href="#installation"><strong> Installation </strong></a> |
    <a href="#usage"><strong> Usage </strong></a> |
    <a href="#roadmap"><strong> Roadmap </strong></a>


   </p>
<p align="center">

<p align="center">
<a href="https://pypi.org/project/pgapi/"><img src="https://img.shields.io/pypi/v/pgapi?label=PyPI"></a>
<a href="https://github.com/Florents-Tselai/pgAPI/actions/workflows/test.yml?branch=pgapi"><img src="https://github.com/Florents-Tselai/pgAPI/actions/workflows/test.yml/badge.svg"></a>
<a href="https://codecov.io/gh/Florents-Tselai/pgAPI"><img src="https://codecov.io/gh/Florents-Tselai/pgAPI/branch/pgapi/graph/badge.svg"></a>  
<a href="https://opensource.org/licenses/Apache Software License 2.0"><img src="https://img.shields.io/badge/Apache Software License 2.0.0-blue.svg"></a>
<a href="https://github.com/Florents-Tselai/pgAPI/releases"><img src="https://img.shields.io/github/v/release/Florents-Tselai/pgAPI?include_prereleases&label=changelog"></a>

## Inspiration

[sqlite-utils](https://github.com/simonw/sqlite-utils) provides a beautiful
Pythonic [API](https://sqlite-utils.datasette.io/en/stable/reference.html) on
top of `SQLite` databases.
**pgAPI** is an attempt to lift-and-shift that API and replicate it on top of
Postgres instead.

## Installation

```bash
pip install pgAPI
```

## Usage

### Development

```bash
pip install -e '.[test]'
pytest
```

## Roadmap

### v0.1.0

* MVP around `pgapi.Database` to have basic interaction with Postgres,
and be able to run queries returned in Pythonic formats.
* Tests should pass even if that means minimal coverage
* CLI should be disabled
* docs should be disabled or
