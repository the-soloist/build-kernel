#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from lib.compress import unbz2
from lib.config import KERNEL_ROOTFS, WORK_HOME
from lib.download import dl_busybox
from lib.logger import log
from lib.path import init_dir, init_file, copy_file
from lib.system import CMD


class RootFsBuilder(object):
    def __init__(self, busybox_version=None):
        self.busybox_version = busybox_version
        self.busybox_name = None
        self.busybox_path = None

    def import_args(self, args: ArgumentParser):
        self.busybox_version = args.busybox_version
        self.busybox_name = f"busybox-{self.busybox_version}"
        self.busybox_path = KERNEL_ROOTFS / self.busybox_name
        self.rootfs_path = self.busybox_path / "_install"

    def download(self):
        res = dl_busybox(self.busybox_version)
        if res == True:
            log.info(f"decompress {self.busybox_name}.tar.bz2")
            unbz2(KERNEL_ROOTFS / f"{self.busybox_name}.tar.bz2", KERNEL_ROOTFS, True)

    def pack_rootfs(self):
        init_dir(self.rootfs_path / "root")
        init_dir(self.rootfs_path / "home/pwn")

        init_path = self.rootfs_path / "init"
        copy_file(WORK_HOME / "scripts/rootfs/init", init_path)
        init_path.chmod(0o755)

        CMD(f"cd {self.rootfs_path} && find . | cpio -o --format=newc > ../../rootfs.cpio")
