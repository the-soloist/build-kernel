#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
from pathlib import Path

from lib.logger import log


def init_dir(dir_path: Path):
    if not dir_path.is_dir():
        dir_path.mkdir(parents=True, exist_ok=True)


def init_file(file_path: Path):
    if not file_path.is_file():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()


def clear_file(file_path: Path):
    if file_path.is_file():
        file_path.unlink()


def move_file(src: Path, dst: Path):
    shutil.move(src, dst)


def copy_file(src: Path, dst: Path, root: Path = None):
    log.debug(f"copy {src} to {dst}")

    if src.is_file():
        shutil.copy(src, dst)
    else:
        msg = str(src.relative_to(root)) if root else str(src)
        log.warning(f"{msg} not found.")
