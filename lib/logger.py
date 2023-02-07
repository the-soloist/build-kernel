#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import json
import sys
from loguru import logger as log
from pathlib import Path

from lib.config import CONFIG


log_path = Path(CONFIG.get("general", "log_path")) / "build.log"
if not log_path.is_file():
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.touch()

# 终端日志输出格式
stdout_fmt = (
    "<cyan>{time:HH:mm:ss}</cyan> "
    "[<level>{level: >8}</level>] "
    "<blue>{module}</blue>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# 日志文件记录格式
logfile_fmt = (
    "<light-green>{time:YYYY-MM-DD HH:mm:ss.SSS}</light-green> "
    "[<level>{level: >8}</level>] "
    "<blue>{module}</blue>.<blue>{function}</blue>:"
    "<blue>{line}</blue> - <level>{message}</level>"
)

log.remove()

# 如果你想在命令终端静默运行，可以将以下一行中的 level 设置为 QUITE
log.add(sys.stderr, level="INFO", format=stdout_fmt, enqueue=True)  # 命令终端日志级别默认为INFOR
log.add(log_path, level="TRACE", format=logfile_fmt, enqueue=True, encoding="utf-8")  # 日志文件默认为级别为DEBUG


if __name__ == "__main__":
    log.trace("test trace")
    log.debug("test debug")
    log.info("test info")
    log.success("test success")
    log.warning("test warning")
    log.error("test error")
    log.critical("test critical")
