#!/usr/bin/env bash
set -x

qemu-system-x86_64 \
    -m 256M -smp 4,cores=2,threads=2 \
    -kernel ./bzImage \
    -initrd ./rootfs.cpio \
    -append "root=/dev/ram rw console=ttyS0 oops=panic panic=1 nokaslr" \
    -cpu qemu64 \
    -netdev user,id=t0, -device e1000,netdev=t0,id=nic0 \
    -monitor /dev/null \
    -nographic \
    -s
