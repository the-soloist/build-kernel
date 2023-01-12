# build kernel

编译 Linux Kernel 的小工具

## usage

```
> python build.py -h
usage: build.py [-h] [-P] [-d] [-pk] [-pr] (-kv KERNEL_VERSION | -gc GIT_COMMIT | -gt GIT_TAG | -bv BUSYBOX_VERSION) {kc,rc} ...

positional arguments:
  {kc,rc}               sub command
    kc                  kernel compiler config
    rc                  rootfs compiler config

options:
  -h, --help            show this help message and exit
  -P, --use-proxies
  -d, --download
  -pk, --pack-kernel-files
  -pr, --pack-rootfs-image
  -kv KERNEL_VERSION, --kernel-version KERNEL_VERSION
  -gc GIT_COMMIT, --git-commit GIT_COMMIT
  -gt GIT_TAG, --git-tag GIT_TAG
  -bv BUSYBOX_VERSION, --busybox-version BUSYBOX_VERSION
```

```sh
# 下载 kernel 源码
python build.py -kv 5.17.11 -d
# 使用代理下载 kernel 源码
python build.py -P -kv 5.17.11 -d
# 使用16个线程，内置编译选项，编译 kernel
python build.py -kv 5.17.11 kc -s -t 16
# 下载 busybox 源码
python build.py -bv 1.35.0 -d
# 使用内置编译选项编译 busybox
python build.py -bv 1.35.0 rc -s
# 打包 busybox 文件系统位 cpio
python build.py -bv 1.35.0 -pr
# 打包 kernel 文件+文件系统+调试脚本
python build.py -kv 5.17.11 -pk
```
