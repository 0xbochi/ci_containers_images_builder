#!/bin/bash
# Run inside the freshly built image by the CI before it is pushed.
set -euxo pipefail

for tool in i686-elf-gcc i686-elf-g++ i686-elf-as i686-elf-ld nasm make qemu-system-i386 gdb; do
    command -v "$tool"
done

# Cross-compile a freestanding object and check it is really 32-bit ELF
cd "$(mktemp -d)"
echo 'int main(void) { return 0; }' > t.c
i686-elf-gcc -ffreestanding -nostdlib -c t.c -o t.o
i686-elf-objdump -f t.o | grep -q 'file format elf32-i386'

# Must not run as root
test "$(id -u)" != 0
