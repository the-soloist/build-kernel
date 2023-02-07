#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from argparse import ArgumentParser

from lib.config import CONFIG, BUILD_JSON_CONF
from lib.core import KernelBuilder
from lib.logger import log
from lib.path import clear_file
from lib.system import CMD
from lib.utils import parse_compile_options
from lib.number import Version


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
                # check compile version
                if not self.check_version_expression(conf["version"]):
                    log.error("version check error")
                    exit(1)

                # set options
                for opt in conf["options"]:
                    k, v = opt.split("=")
                    self.edit_option(k, v)

                # set debug options
                if conf["debug"] == True:
                    self.add_debug_options()

                return True

        log.error(f"{self.json_config} is not in build.json")
        exit(1)

    def check_version_expression(self, version_dict: dict):
        if self.builder.kernel_version:
            key = "kernel_version"
        elif self.builder.git_commit:
            key = "git_commit"
        elif self.builder.git_tag:
            key = "git_tag"

        vlist = version_dict.get(key)
        bv = getattr(self.builder, key)
        log.info(f"compare {bv} with {vlist}")

        # when `vlist` is empty, it means that the version is unlimited
        if not vlist:
            return True

        # parse arithmetic expressions
        if key == "git_commit":
            if bv in vlist:
                return True
        else:  # key == "kernel_version" or key == "git_tag"
            for v in vlist:
                if v.startswith(">") and v[1] != "=":
                    if Version(bv) > Version(v):
                        return True
                elif v.startswith(">="):
                    if Version(bv) >= Version(v):
                        return True
                elif v.startswith("<") and v[1] != "=":
                    if Version(bv) < Version(v):
                        return True
                elif v.startswith("<="):
                    if Version(bv) <= Version(v):
                        return True
                elif "~" in v:
                    _v1, _v2 = v.split("~")
                    if Version(_v1) <= Version(bv) <= Version(_v2):
                        return True
                else:
                    if Version(bv) == Version(v):
                        return True

        return False

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
