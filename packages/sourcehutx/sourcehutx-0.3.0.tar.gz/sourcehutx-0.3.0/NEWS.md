<!--
Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
SPDX-License-Identifier: MIT
-->

NEWS
======

## 0.3.0 - 2023-12-20 <a id='0.3.0'></a>

### Added

- all: add more docstrings
- git: add `HEAD` and `readme` fields to the `Repository` model
- git: add `RepositoryRef` model and `GitSrhtClient.get_repository_ref()`
  method to return a minimal reference to a repository.

### Fixed

- all: ignore pydantic v2 DeprecationWarnings

## 0.2.0 - 2023-12-02 <a id='0.2.0'></a>

### Added

- all: add `get_user_ref()` and `__all__` for all services
- builds: add `runner` and `owner` members to `Job`
- builds: add `list_secrets()`

### Fixed

- exceptions: make `SrhtClientError` inherit `SrhtError`
- all: fix pydantic `GenericBeforeBaseModelWarning`s

## 0.1.0 - 2023-08-27 <a id='0.1.0'></a>

### Added

- todo: add support for managing tracker ACLs

## 0.0.2 - 2023-08-26 <a id='0.0.2'></a>

### Fixed

- add py.typed marker
- fix specfile typo

## 0.0.1 - 2023-08-26 <a id='0.0.1'></a>

### Summary

Initial release

These services are currently supported:

- builds
- git
- lists
- meta
- pages
- paste
- todo

