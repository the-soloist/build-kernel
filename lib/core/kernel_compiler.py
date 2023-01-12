#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from argparse import ArgumentParser

from lib.config import CONFIG, BUILD_JSON_CONF
from lib.core import KernelBuilder
from lib.logger import log
from lib.path import clear_file
from lib.system import CMD
from lib.utils import parse_compile_options


class KernelCompiler(object):
    def __init__(self):
        self.builder: KernelBuilder = None

        self.thread_number = None
        self.add_debug_symbol = None     # 添加调试符号
        self.set_default_options = None  # 添加默认配置

        self.custom_config_path = None   # 使用自定义配置文件
        self.ini_config = None
        self.json_config = None

        self.build_arch = CONFIG["compile_kernel"]["arch"]
        self.dot_config_path = None  # .config 路径
        self.dot_config = None       # .config 内容
        self.new_dot_config = None   # 更新后的 .config 内容
        self.compile_options = {}    # 自定义编译参数

    def import_args(self, args: ArgumentParser):
        self.thread_number = args.thread_number

        self.add_debug_symbol = args.add_debug_symbol
        self.set_default_options = args.set_default_options

        self.custom_config_path = args.custom_config_path
        self.ini_config = args.ini_config
        self.json_config = args.json_config

    def set_builder(self, builder: KernelBuilder):
        self.builder = builder

    def compile_kernel(self):
        self.init_dot_config()  # 初始化 .config

        if self.set_default_options:
            self.set_default_compile_options()

        if self.ini_config:
            # 从 ini 中读取 kernel option
            self.get_options_from_ini()
        elif self.json_config:
            # 从 json 中读取 kernel option
            self.get_options_from_json()
        else:
            pass

        if self.add_debug_symbol:  # 添加调试符号
            self.add_debug_options()

        self.read_dot_config()
        self.parse_compile_options()
        self.write_dot_config()

        # 编译
        CMD(f"make --directory={self.builder.src_path} -j{self.thread_number} vmlinux bzImage", pause=True)

    """ option manager """

    def edit_option(self, key, value):
        self.compile_options[key] = value

    def add_debug_options(self):
        self.compile_options["CONFIG_DEBUG_INFO"] = "y"
        self.compile_options["CONFIG_DEBUG_INFO_DWARF4"] = "y"
        self.compile_options["CONFIG_DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT"] = "y"
        self.compile_options["CONFIG_GDB_SCRIPTS"] = "y"

    def set_default_compile_options(self):
        self.compile_options["CONFIG_DEBUG_INFO"] = "y"
        self.compile_options["CONFIG_DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT"] = "y"

    def get_options_from_ini(self):
        """ TODO 解析 ini 中的 kernel config """
        pass

    def get_options_from_json(self):
        """ 解析 json 中的 kernel config """
        json_conf = json.load(open(BUILD_JSON_CONF, "r"))

        for conf in json_conf["kernel_config"]:
            if self.json_config == conf["name"]:
                for opt in conf["options"]:
                    k, v = opt.split("=")
                    self.edit_option(k, v)

                if conf["name"]["debug"] == True:
                    self.add_debug_options()

                return True

        log.error(f"{self.json_config} is not in build.json")
        exit(-1)

    def parse_compile_options(self):
        self.new_dot_config = parse_compile_options(self.dot_config, self.compile_options)

    """ config manager """

    def init_dot_config(self):
        self.dot_config_path = self.builder.src_path / ".config"
        clear_file(self.dot_config_path)

        if self.custom_config_path:
            copy_file(Path(self.custom_config_path), self.dot_config_path)
        else:
            CMD(f"make --directory={self.builder.src_path} {self.build_arch}_defconfig")

    def read_dot_config(self):
        """ 读取 .config 内容 """
        self.dot_config = open(self.dot_config_path, "r").read()

    def write_dot_config(self):
        """ 写入 .config """
        open(self.dot_config_path, "w").write(self.new_dot_config)
