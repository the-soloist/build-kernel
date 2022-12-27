#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from pathlib import Path

from lib.compress import ungz, unzip
from lib.config import CONFIG, WORK_HOME, KERNEL_SOUECE, KERNEL_IMAGES, KERNEL_ROOTFS
from lib.download import dl_kernel_version, dl_git_commit, dl_git_tag
from lib.logger import log
from lib.path import init_dir, copy_file


START_SH = """
#!/usr/bin/env bash
set -x

qemu-system-{arch} \\
    -m {memory} -smp {smp} \\
    -kernel ./bzImage \\
    -initrd ./rootfs.cpio \\
    -append "{append}" \\
    -cpu {cpu} \\
    -netdev user,id=t0, -device e1000,netdev=t0,id=nic0 \\
    -no-reboot \\
    -nographic
""".strip()


class KernelBuilder(object):
    def __init__(self, kernel_version=None, git_commit=None, git_tag=None):
        self.kernel_version = kernel_version
        self.git_commit = git_commit
        self.git_tag = git_tag

        self.build_arch = CONFIG["compile_kernel"]["arch"]
        self.kernel_name = None
        self.src_path: Path = None

    def import_args(self, args: ArgumentParser):
        self.kernel_version = args.kernel_version
        self.git_commit = args.git_commit
        self.git_tag = args.git_tag

        if self.kernel_version:
            self.kernel_name = f"linux-{self.kernel_version}"
        elif self.git_commit:
            self.kernel_name = f"linux-{self.git_commit}"
        elif self.git_tag:
            self.kernel_name = f"linux-{self.git_tag}"
        else:
            log.error("kernel_name init failed!")
            exit(-1)

        self.src_path = KERNEL_SOUECE / self.kernel_name
        self.image_path = KERNEL_IMAGES / self.kernel_name

    def download(self):
        if self.kernel_version:
            res = dl_kernel_version(self.kernel_version)
            if res == True:
                log.info(f"decompress {self.kernel_name}.tar.gz")
                ungz(KERNEL_SOUECE / f"{self.kernel_name}.tar.gz", KERNEL_SOUECE, True)

        elif self.git_commit:
            res = dl_git_commit(self.git_commit)
            if res == True:
                log.info(f"decompress {self.kernel_name}.zip")
                unzip(KERNEL_SOUECE / f"{self.kernel_name}.zip", KERNEL_SOUECE, True)

        elif self.git_tag:
            res = dl_git_tag(self.git_tag)
            if res == True:
                log.info(f"decompress {self.kernel_name}.gz")
                ungz(KERNEL_SOUECE / f"{self.kernel_name}.gz", KERNEL_SOUECE, True)

        else:
            log.error("not found kernel download method.")
            exit(-1)

        return self.kernel_name

    def write_start_sh(self):
        start_sh = START_SH

        arch = CONFIG["compile_kernel"]["arch"]
        memory = CONFIG["qemu_config"]["memory"]
        cpu = CONFIG["qemu_config"]["cpu"]
        smp = CONFIG["qemu_config"]["smp"]

        append_list = ["root=/dev/ram", "rw", "console=ttyS0", "oops=panic", "panic=1"]
        append_list.append("kaslr" if CONFIG["qemu_config"]["kaslr"] == "yes" else "nokaslr")

        if CONFIG["qemu_config"]["gdb"] == "yes":
            port = CONFIG["qemu_config"]["port"]
            start_sh += " -gdb tcp::{port}".format(port=port)
            # start_sh += " -s"

        # import ipdb
        # ipdb.set_trace()
        start_sh = start_sh.format(
            arch=arch,
            memory=memory,
            cpu=cpu,
            smp=smp,
            append=" ".join(append_list)
        )

        start_sh_path = self.image_path / "start.sh"
        open(start_sh_path, "w").write(start_sh)
        start_sh_path.chmod(0o755)

    def pack_kernel_files(self):
        init_dir(self.image_path)
        init_dir(self.image_path / "scripts")
        init_dir(self.image_path / "exploit")

        # === COPY KERNEL FILES ===
        # copy vmlinux
        log.info(f"copy vmlinux to {self.kernel_name}")
        copy_file(self.src_path / "vmlinux", self.image_path)

        # copy bzImage
        log.info(f"copy bzImage to {self.kernel_name}")
        if self.build_arch.startswith("x86"):
            bzimage_path = self.src_path / "arch/x86/boot/bzImage"
        else:
            bzimage_path = self.src_path / f"arch/{self.build_arch}/boot/bzImage"
        copy_file(bzimage_path, self.image_path)

        # === COPY ROOTFS ===
        log.info(f"copy rootfs to {self.kernel_name}")
        copy_file(KERNEL_ROOTFS / "rootfs.cpio", self.image_path)

        # === COPY DEBUG SCRIPTS ===
        log.info(f"copy scripts to {self.kernel_name}")

        copy_file(WORK_HOME / "scripts/rootfs/vmmap", self.image_path)

        copy_file(WORK_HOME / "scripts/debug/run.sh", self.image_path)
        copy_file(WORK_HOME / "scripts/debug/debug.sh", self.image_path)
        copy_file(WORK_HOME / "scripts/debug/Makefile", self.image_path)

        copy_file(WORK_HOME / "scripts/misc/extract-vmlinux", self.image_path / "scripts")
        copy_file(WORK_HOME / "scripts/misc/pack-cpio.sh", self.image_path / "scripts")
        copy_file(WORK_HOME / "scripts/misc/unpack-cpio.sh", self.image_path / "scripts")

        self.write_start_sh()  # self.image_path / "start.sh"
