#!/usr/bin/env bash
set -ex

uv run mypy "${@:-.}"