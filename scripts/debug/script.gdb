file "vmlinux"
# set architecture i386:x86-64:intel
target remote localhost:1234

set $text = 0xffffffffc0201000
set $bss = 0xffffffffc02036c0
set $data = 0xffffffffc0203020
set $symtab = 0xffffffffc0207008
set $strtab = 0xffffffffc02076b0

add-symbol-file ./rootfs/ker.ko -s .text $text
add-symbol-file ./rootfs/ker.ko -s .bss $bss
add-symbol-file ./rootfs/ker.ko -s .data $data
add-symbol-file ./rootfs/ker.ko -s .symtab $symtab
add-symbol-file ./rootfs/ker.ko -s .strtab $strtab

# b start_kernel
continue
# tele *(void**)($bss+8)