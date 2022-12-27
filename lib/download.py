#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from argparse import ArgumentParser
from pathlib import Path
from tqdm import tqdm

from lib.config import CONFIG, PROXISE, KERNEL_SOUECE, KERNEL_ROOTFS
from lib.logger import log
from lib.path import clear_file


def dl_kernel_version(version):
    url = CONFIG["kernel_dl"]["version_url"]

    if int(version.split(".")[0]) < 3 or ".".join(version.split(".")[:-1]) == "3.0":
        v1 = ".".join(version.split(".")[:-1])
    else:
        v1 = version.split(".")[0] + ".x"

    v2 = version
    url = url.format(v1, v2)

    log.info("download linux kernel, url: " + url)

    res = requests.get(url, stream=True, proxies=PROXISE)
    total_size = int(res.headers.get('content-length', 0))

    kernel_name = f"linux-{v2}"

    # 避免重复下载
    src_path = KERNEL_SOUECE / kernel_name
    if src_path.is_dir():
        log.warning(f"{str(src_path)} already exists.")
        return False

    file_path = KERNEL_SOUECE / f"{kernel_name}.tar.gz"
    clear_file(file_path)

    with open(file_path, "wb") as fp, tqdm(desc=file_path.name, total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as bar:
        for data in res.iter_content(chunk_size=1024):
            size = fp.write(data)
            bar.update(size)

    return True


def dl_git_commit(commit):
    url = CONFIG["kernel_dl"]["git_commit_url"]
    url = url.format(commit)

    log.info("download linux kernel, url: " + url)

    res = requests.get(url, stream=True, proxies=PROXISE)
    total_size = int(res.headers.get('content-length', 0)) // 1024

    kernel_name = f"linux-{commit}"

    # 避免重复下载
    src_path = KERNEL_SOUECE / kernel_name
    if src_path.is_dir():
        log.warning(f"{str(src_path)} already exists.")
        return False

    file_path = KERNEL_SOUECE / f"{kernel_name}.zip"
    clear_file(file_path)

    with open(file_path, "wb") as fp, tqdm(desc=file_path.name, total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as bar:
        for data in res.iter_content(chunk_size=1024):
            size = fp.write(data)
            bar.update(size)

    return True


def dl_git_tag(tag):
    url = CONFIG["kernel_dl"]["git_tag_url"]
    url = url.format(tag)

    log.info("download linux kernel, url: " + url)

    res = requests.get(url, stream=True, proxies=PROXISE)
    total_size = int(res.headers.get('content-length', 0)) // 1024

    kernel_name = f"linux-{tag}"

    # 避免重复下载
    src_path = KERNEL_SOUECE / kernel_name
    if src_path.is_dir():
        log.warning(f"{str(src_path)} already exists.")
        return False

    file_path = KERNEL_SOUECE / f"{kernel_name}.gz"
    clear_file(file_path)

    with open(file_path, "wb") as fp, tqdm(desc=file_path.name, total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as bar:
        for data in res.iter_content(chunk_size=1024):
            size = fp.write(data)
            bar.update(size)

    return True


def dl_busybox(version):
    url = CONFIG["rootfs_dl"]["busybox_url"]
    url = url .format(version)

    log.info("download busybox, url: " + url)

    res = requests.get(url, stream=True, proxies=PROXISE)
    total_size = int(res.headers.get('content-length', 0)) // 1024

    busybox_name = f"busybox-{version}"

    # 避免重复下载
    src_path = KERNEL_ROOTFS / busybox_name
    if src_path.is_dir():
        log.warning(f"{str(src_path)} already exists.")
        return False

    file_path = KERNEL_ROOTFS / f"{busybox_name}.tar.bz2"
    clear_file(file_path)

    with open(file_path, "wb") as fp, tqdm(desc=file_path.name, total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as bar:
        for data in res.iter_content(chunk_size=1024):
            size = fp.write(data)
            bar.update(size)

    return True
