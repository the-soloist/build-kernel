#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import configparser
from pathlib import Path

from lib.path import init_dir


def init_parser() -> argparse.ArgumentParser:
    # init parser
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help="sub command")

    parser.add_argument("-P", "--use-proxies", action="store_true", default=False)
    parser.add_argument("-d", "--download", action="store_true", default=False)
    parser.add_argument("-pk", "--pack-kernel-files", action="store_true", default=False)
    parser.add_argument("-pr", "--pack-rootfs-image", action="store_true")

    # kernel/rootfs builder
    krb_group = parser.add_mutually_exclusive_group(required=True)
    krb_group.add_argument("-kv", "--kernel-version", action="store")
    krb_group.add_argument("-gc", "--git-commit", action="store")
    krb_group.add_argument("-gt", "--git-tag", action="store")
    krb_group.add_argument("-bv", "--busybox-version", action="store")

    # kernel compiler
    kc_parser = subparsers.add_parser("kc", help="kernel compiler config")
    kc_parser.add_argument("-t", "--thread-number", action="store", type=int, default=4, help="set compiler's thread number (default: 4)")
    kc_parser.add_argument("-d", "--add-debug-symbol", action="store_true")
    kc_parser.add_argument("-s", "--set-default-options", action="store_true")
    kc_group = kc_parser.add_mutually_exclusive_group(required=False)
    kc_group.add_argument("-c", "--custom-config-path", action="store")
    kc_group.add_argument("-i", "--ini-config", action="store")
    kc_group.add_argument("-j", "--json-config", action="store")

    # rootfs compiler
    rc_parser = subparsers.add_parser("rc", help="rootfs compiler config")
    rc_parser.add_argument("-t", "--thread-number", action="store", type=int, default=4, help="set compiler's thread number (default: 4)")
    rc_parser.add_argument("-s", "--set-default-options", action="store_true")

    return parser


# === init args parser ===
parser = init_parser()


# === init dirs ===
WORK_HOME = Path(__file__).parent.parent

KERNEL_IMAGES = WORK_HOME / "kernel" / "images"
KERNEL_ROOTFS = WORK_HOME / "kernel" / "rootfs"
KERNEL_SOUECE = WORK_HOME / "kernel" / "source"

BUILD_INI_CONF = WORK_HOME / "build.ini"
BUILD_JSON_CONF = WORK_HOME / "build.json"

init_dir(KERNEL_IMAGES)
init_dir(KERNEL_ROOTFS)
init_dir(KERNEL_SOUECE)


# === init config parser ===
CONFIG = configparser.ConfigParser()
CONFIG.read(BUILD_INI_CONF, encoding="utf-8")


# === init http config ===
PROXISE = {}
