#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import configparser
from pathlib import Path


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
    kc_parser.add_argument("-t", "--thread-number", action="store", type=int, default=4, help="sets the number of compilation threads (default: 4)")
    kc_parser.add_argument("-m", "--copy-dot-config", action="store_true", help="copy .config")
    kc_parser.add_argument("-d", "--add-debug-symbol", action="store_true", help="add debugging options")
    kc_parser.add_argument("-s", "--set-default-options", action="store_true", help="set built-in default options")
    kc_group = kc_parser.add_mutually_exclusive_group(required=False)
    kc_group.add_argument("-c", "--custom-config-path", action="store", help="use custom config path")
    kc_group.add_argument("-i", "--ini-config", action="store", help="use the configuration in JSON")
    kc_group.add_argument("-j", "--json-config", action="store", help="use the configuration in INI")

    # rootfs compiler
    rc_parser = subparsers.add_parser("rc", help="rootfs compiler config")
    rc_parser.add_argument("-t", "--thread-number", action="store", type=int, default=4, help="sets the number of compilation threads (default: 4)")
    rc_parser.add_argument("-m", "--copy-dot-config", action="store_true", help="copy .config")
    rc_parser.add_argument("-s", "--set-default-options", action="store_true", help="set built-in default options")
    rc_group = rc_parser.add_mutually_exclusive_group(required=False)
    rc_group.add_argument("-c", "--custom-config-path", action="store", help="use custom config path")

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


# === init config parser ===
CONFIG = configparser.ConfigParser()
CONFIG.read(BUILD_INI_CONF, encoding="utf-8")


# === init http config ===
PROXISE = {}
