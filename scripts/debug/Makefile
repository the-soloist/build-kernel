ALL:
	gcc --static -O0 exploit/exp.c -o rootfs/exp
	cd rootfs && find . | cpio -o --format=newc > ../rootfs.cpio
