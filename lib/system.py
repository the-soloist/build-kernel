#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

from lib.logger import log


def CMD(cmd, pause=False):
    log.info(f"cmd: {cmd}")

    if pause:
        PAUSE()

    os.system(cmd)


def POPEN():
    pass


def PAUSE(n=None):
    if n is None:
        log.warning('Paused (press enter to continue)')
        input('')
    else:
        raise ValueError('PAUSE(): n must be a number or None')
