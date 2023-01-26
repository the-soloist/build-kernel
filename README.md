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
python build.py -kv 5.17.11 kc -t 16 -s
# 使用16个线程，json 配置 test-config，编译 kernel
python build.py -kv 5.17.11 kc -t 16 -j "test-config"

# 下载 busybox 源码
python build.py -bv 1.35.0 -d
# 使用内置编译选项编译 busybox
python build.py -bv 1.35.0 rc -s
# 打包 busybox 文件系统位 cpio
python build.py -bv 1.35.0 -pr

# 打包 kernel 文件+文件系统+调试脚本
python build.py -kv 5.17.11 -pk
```

可以在 bashrc 中添加一个 alias，方便使用

```sh
alias build-kernel="python /path/to/build-kernel/build.py"
```

## custom

`build.json` 中可以自定义添加 kernel 编译的配置，格式如下

```json
{
  "kernel_config": [
    {
      "name": "test",
      "version": {
        "kernel_version": ["<0.1.1"],
        "git_commit": [],
        "git_tag": []
      },
      "options": ["CONFIG_IP_NF_*=y", "CONFIG_E1000=y", "CONFIG_E1000E=y"],
      "debug": false
    }
  ]
}
```

参数解释：

- kernel_config：列表
  - name：配置名
  - version：限定编译版本号，元素之间相当于`或`。根据 `-kv`/`-gc`/`-gt` 参数自动选择对应的 version 列表
    - 支持算数比较 `<`、`<=`、`>`、`>=`
    - `a1~a2` 表示从匹配从 a1 到 a2 之间的版本号（`a1<=x<=a2`）
    - 不添加比较符，表示匹配单一版本号
    - 参数为空列表，表示不限制版本号，跳过检查
  - options：自定义编译选项
    - 支持 `*` 通配符
  - debug：开启调试选项
