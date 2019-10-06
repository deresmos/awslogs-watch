awslogs-watch
==

[![Build Status](https://travis-ci.org/deresmos/awslogs-watch.svg?branch=master)](https://travis-ci.org/deresmos/awslogs-watch)
[![PyPI](https://badge.fury.io/py/awslogs-watch.svg)](https://badge.fury.io/py/awslogs-watch)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/deresmos/awslogs-watch/blob/master/LICENSE)


Abount
===
awslogs-watch is a CLI tool that makes it easy to use awslogs.
Default cache directory is `~/.cache/awslogs_watch`

Installation
==
To install awslogs-watch, use pip.

```bash
pip install awslogs_watch
```

Examples
==

## Update awglogs groups cache
```bash
$ awslogs-watch
Input Command: update
```

or

```bash
$ awslogs-watch --update
```

## Get awslogs
```bash
$ awslogs-watch
Input Command: get
Input group: select interactive group name
```

or

```bash
$ awslogs-watch --get
Input group: select interactive group name
```

## Tail awslogs
```bash
$ awslogs-watch
Input Command: tail
Input group: select interactive group name
```

or

```bash
$ awslogs-watch --tail
Input group: select interactive group name
```

## Change profile
```bash
$ awslogs-watch --profile develop
```

## Set awslogs option
```bash
$ awslogs-watch --options="-S"
```
