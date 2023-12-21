# check-iso8601-version-string
A tool (and pre-commit hook) to check that ISO 8601 version strings are valid, and set to today's date.


## Installation
```
python -m pip install check-iso8601-version-string
```

## As a pre-commit hook
See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions.

Sample [`.pre-commit-config.yaml`](https://github.com/simonrob/check-iso8601-version-string/blob/main/pre-commit-config.yaml):

```yaml
repos:
-   repo: https://github.com/simonrob/check-iso8601-version-string
    rev: v2023-12-20
    hooks:
    -   id: check-iso8601-version-string
```
