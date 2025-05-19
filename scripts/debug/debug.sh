#!/usr/bin/env bash
set -x

GDB_SCRIPT_PATH="/tmp/tmp_dbg_kernel_script.gdb"
DRIVER_PATH="$(pwd)/driver.ko"

cat <<EOF >$GDB_SCRIPT_PATH
file "vmlinux"
# set architecture i386:x86-64:intel
# add-symbol-file "$DRIVER_PATH" 0xffffffffc0000000
target remote localhost:1234

# b start_kernel
# continue
EOF

gdb -ex "source $GDB_SCRIPT_PATH"
