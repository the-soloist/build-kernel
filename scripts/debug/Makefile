ALL:
	gcc --static -masm=intel -O0 exp.c -o rootfs/exp
	cd rootfs && find . | cpio -o --format=newc > ../rootfs.cpio
