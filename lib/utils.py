#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from lib.logger import log


def parse_compile_options(config: str, options: dict):
    """ 根据 compile_options 替换实际的 config 内容 """

    new_config_list = []

    # 第一轮遍历 .config 内容
    for line in config.split("\n"):
        conf = line

        # 跳过一些无意义的注释
        ll = [x for x in re.split("[ =#]", line) if x]
        if len(ll) == 0:
            new_config_list.append(conf)
            continue
        else:
            key = ll[0]

        # 添加自定义 option，添加成功后跳过该轮 for 循环
        if key in list(options.keys()):
            conf = f"{key}={options[key]}"
            new_config_list.append(conf)
            log.info(f"set custom option: {conf}")

            options.pop(key)
            continue

        # 添加带 * 的 option
        for opt_key in options.keys():
            if opt_key[-1] != "*":
                continue

            # 匹配 * 前的部分，匹配成功后仅更新 conf 变量，在外面的大循环中进行 append
            if key.startswith(opt_key[:-1]):
                conf = f"{key}={options[opt_key]}"
                log.info(f"set custom * option: {conf}")
                break

        new_config_list.append(conf)

    # 添加余下的 option
    if len(options.keys()) != 0:
        for key in options.keys():
            # 跳过 * option
            if key[-1] == "*":
                continue

            conf = f"{key}={options[key]}"
            new_config_list.append(conf)
            log.info(f"set unfound option: {conf}")

    return "\n".join(new_config_list)
