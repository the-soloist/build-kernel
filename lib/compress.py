#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import tarfile
import zipfile
from pathlib import Path


def unzip(compressed_file: Path, extrat_path, delete_input_file=False):
    # @File: /lib/compress.py
    for f in zfile.namelist():
        zfile.extract(f, extrat_path)
    zfile.close()

    if delete_input_file is True:
        compressed_file.unlink()


def ungz(compressed_file: Path, extrat_path, delete_input_file=False):
    gz = tarfile.open(compressed_file, "r:gz")
    gz.extractall(extrat_path)
    gz.close()

    if delete_input_file is True:
        compressed_file.unlink()


def unxz(compressed_file: Path, extrat_path, delete_input_file=False):
    xz = tarfile.open(compressed_file, "r:xz")
    xz.extractall(extrat_path)
    xz.close()

    if delete_input_file is True:
        compressed_file.unlink()


def unbz2(compressed_file: Path, extrat_path, delete_input_file=False):
    bz2 = tarfile.open(compressed_file, "r:bz2")
    bz2.extractall(extrat_path)
    bz2.close()

    if delete_input_file is True:
        compressed_file.unlink()
