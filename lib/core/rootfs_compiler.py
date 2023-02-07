#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from pathlib import Path

from lib.core.rootfs_builder import RootFsBuilder
from lib.path import clear_file, copy_file
from lib.system import CMD
from lib.utils import parse_compile_options


class RootFsCompiler(object):
    def __init__(self):
        self.builder: RootFsBuilder = None

        self.thread_number = None
        self.set_default_options = None  # 添加默认配置

        self.dot_config_path = None  # .config 路径
        self.dot_config = None       # .config 内容
        self.new_dot_config = None   # 更新后的 .config 内容
        self.compile_options = {}    # 自定义编译参数

    def import_args(self, args: ArgumentParser):
        self.thread_number = args.thread_number

        self.copy_dot_config = args.copy_dot_config
        self.set_default_options = args.set_default_options

        self.custom_config_path = args.custom_config_path

    def set_builder(self, builder: RootFsBuilder):
        self.builder = builder

    def compile_busybox(self):
        self.init_dot_config()

        if self.copy_dot_config:
            # 拷贝 .config 并返回
            return copy_file(self.dot_config_path, Path("./dot_config"))

        if self.set_default_options:
            self.set_default_compile_options()

        self.read_dot_config()
        self.parse_compile_options()
        self.write_dot_config()

        CMD(f"make --directory={self.builder.busybox_path} -j{self.thread_number}", pause=True)
        CMD(f"make --directory={self.builder.busybox_path} install", pause=True)

    """ option manager """

    def edit_option(self, key, value):
        self.compile_options[key] = value

    def set_default_compile_options(self):
        # Build static binary
        self.compile_options["CONFIG_STATIC"] = "y"
        # NFS file systems on Linux
        self.compile_options["CONFIG_FEATURE_MOUNT_NFS"] = "n"
        # inetd
        self.compile_options["CONFIG_INETD"] = "n"
        self.compile_options["CONFIG_FEATURE_INETD_SUPPORT_BUILTIN_ECHO"] = "n"
        self.compile_options["CONFIG_FEATURE_INETD_SUPPORT_BUILTIN_DISCARD"] = "n"
        self.compile_options["CONFIG_FEATURE_INETD_SUPPORT_BUILTIN_TIME"] = "n"
        self.compile_options["CONFIG_FEATURE_INETD_SUPPORT_BUILTIN_DAYTIME"] = "n"
        self.compile_options["CONFIG_FEATURE_INETD_SUPPORT_BUILTIN_CHARGEN"] = "n"

    def parse_compile_options(self):
        self.new_dot_config = parse_compile_options(self.dot_config, self.compile_options)

    """ config manager """

    def init_dot_config(self):
        self.dot_config_path = self.builder.busybox_path / ".config"
        clear_file(self.dot_config_path)

        if self.custom_config_path:
            copy_file(Path(self.custom_config_path), self.dot_config_path)
        else:
            CMD(f"make --directory={self.builder.busybox_path} defconfig")

    def read_dot_config(self):
        """ 读取 .config 内容 """
        self.dot_config = open(self.dot_config_path, "r").read()

    def write_dot_config(self):
        """ 写入 .config """
        open(self.dot_config_path, "w").write(self.new_dot_config)
