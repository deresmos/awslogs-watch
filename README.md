awslogs-watch
==

[![PyPI](https://badge.fury.io/py/awslogs-watch.svg)](https://badge.fury.io/py/awslogs-watch)
[![Python Test](https://github.com/deresmos/awslogs-watch/workflows/Python%20Test/badge.svg)](https://github.com/deresmos/awslogs-watch/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/deresmos/awslogs-watch/blob/master/LICENSE)


About
===
awslogs-watch is a CLI tool that makes it easy to use awslogs.
Default cache directory is `$HOME/.cache/awslogs_watch`

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
Command: update
```

or

```bash
$ awslogs-watch --update
```

## Interactive mode
`option: -i`
```bash
$ awslogs-watch -i
Profile: default
Command: get
Option : --start="1d"
Group  : group_name
```

## Interactive mode (Default value is recent history)
`option: -r`
```bash
$ awslogs-watch -ir
Profile: default
Command: get
Option : --start="1d"
Group  : group_name
```

## Get awslogs
```bash
$ awslogs-watch
Command: get
group: select interactive group name
```

or

```bash
$ awslogs-watch --get
group: select interactive group name
```

## Tail awslogs
```bash
$ awslogs-watch
Command: tail
group: select interactive group name
```

or

```bash
$ awslogs-watch --tail
group: select interactive group name
```

## Change profile
```bash
$ awslogs-watch --profile develop
```

## Set awslogs option
```bash
$ awslogs-watch --option="-S"
```
