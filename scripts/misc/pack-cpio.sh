#!/usr/bin/env bash
set -x

cd rootfs
find . | cpio -o --format=newc >../rootfs.cpio
