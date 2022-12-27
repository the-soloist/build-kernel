#!/usr/bin/env bash
set -x

mkdir rootfs
cp rootfs.cpio rootfs
cd rootfs
cpio -idmv <rootfs.cpio
rm rootfs.cpio
