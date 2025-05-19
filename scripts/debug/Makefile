ALL:
	gcc -Os -static -masm=intel -s exp.c -o rootfs/exp
	cd rootfs && find . | cpio -o --format=newc > ../rootfs.cpio
