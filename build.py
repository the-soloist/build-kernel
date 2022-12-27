#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from lib.config import parser, CONFIG, PROXISE
from lib.core import *
from lib.logger import log


args = parser.parse_args()


def main():
    global PROXISE
    # print(args)

    if args.use_proxies:
        PROXISE = {
            "http": f"http://{CONFIG['proxy']['host']}:{CONFIG['proxy']['port']}",
            "https": f"http://{CONFIG['proxy']['host']}:{CONFIG['proxy']['port']}"
        }
        log.info(f"using proxies: {str(PROXISE)}")

    if not args.busybox_version:
        # kernel builder
        kernel_builder = KernelBuilder()
        kernel_builder.import_args(args)

        if args.download:
            kernel_builder.download()

        # kernel compiler
        if hasattr(args, "set_default_options"):
            kernel_compiler = KernelCompiler()
            kernel_compiler.set_builder(kernel_builder)
            kernel_compiler.import_args(args)
            kernel_compiler.compile_kernel()

        if args.pack_kernel_files:
            kernel_builder.pack_kernel_files()

    else:
        # rootfs builder
        rootfs_builder = RootFsBuilder()
        rootfs_builder.import_args(args)

        if args.download:
            rootfs_builder.download()

        if hasattr(args, "set_default_options"):
            rootfs_compiler = RootFsCompiler()
            rootfs_compiler.set_builder(rootfs_builder)
            rootfs_compiler.import_args(args)
            rootfs_compiler.compile_busybox()

        if args.pack_rootfs_image:
            rootfs_builder.pack_rootfs()


if __name__ == "__main__":
    main()
