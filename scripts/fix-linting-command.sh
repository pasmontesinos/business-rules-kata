#!/usr/bin/env bash
set -ex

uv run ruff format "${@:-.}"
uv run ruff check --fix "${@:-.}"