# Lab 1: Buffer overflows exploit writeup

## Shellcode

The goal of our buffer overflows attack is to unlink (or delete if you want) the
file `home/httpd/grades.txt`. If you are unfamiliar with how to write shellcode,
please check [this article](http://www.phrack.com/issues.html?issue=49&id=14#article)
first before you continue reading this writeup. As the shellcode is usually
being injected into victim program as a string, one important part of writing
shellcode is to avoid the zero byte. This can be eliminated by replacing the
intermediate value `0` into other instructions like `xorl %eax, %eax`, e.t.c.

Now suppose we are going to write shellcode to unlink the `grades.txt` file,
there are two ways to achieve this goal. One is to do syscall with `%eax` equals
to `SYS_unlink (0xa)`, another one is to invoke the C library function `unlink`.
Both two need to take a pointer to a null-terminated C string as the target file
to be unlinked. Since calling `unlink` needs to know the address of this
function in advance, and this is not a trivial task when writing the shellcode,
so we will take the first approach, which will only needs to execute `int $0x80`.

Using the approach described in the above article, we can struct our shellcode
below.

```asm
#define STRING  "/home/httpd/grades.txt"
#define STRLEN  22

main:
jmp  calladdr

popladdr:
  popl %esi
  xorl %eax,%eax           /* get a 32-bit zero value */
  movb %al,(STRLEN)(%esi)  /* null-terminate our string */

  movb $SYS_unlink,%al     /* syscall arg 1: syscall number */
  movl %esi,%ebx           /* syscall arg 2: string pathname */
  int $0x80                /* invoke syscall */

  xorl %ebx,%ebx           /* syscall arg 2: 0 */
  movl %ebx,%eax
  inc %eax                 /* syscall arg 1: SYS_exit (1), uses */
                           /* mov+inc to avoid null byte */
  int $0x80                /* invoke syscall */

calladdr:
  call popladdr
  .ascii STRING
```

`popladdr` and `calladdr` are used to get the address of STRING dynamically, as
we don't know where our shellcode will be injected to. Then the address of
STRING will be loaded into the register `%esi`. We use two instructions
`xorl %eax,%eax` and `movb %al,(STRLEN)(%esi)` instead of `movb $0,(STRLEN)(%esi)`,
this could avoid the byte zero in the generated shellcode. In case of the
`SYS_unlink` fails, `SYS_exit` is called to terminate the program on failure.

## Vulnerability

By browsering `zoobar`'s web server code, we can find several vulnerabilities to
exploit the buffer overflows. Here we only pick two outstanding examples to show
how to exploit it.

The first vulnerability is located in [http.c:105]. `url_decode` does not check
the buffer size of `reqpath`, when the length of `sp1 (URI)` is larger than the
buffer size of `reqpath`, the return address of `process_client` [zookd.c:70]
will be overwritten.

The second vulnerability is located in [http.c:282]. `strcat` does not check the
buffer size of `pn`. Since `handler` is placed ahead of the buffer `pn`, a
carefully constructed `name (URI)` will overwrite the value of `handler`, then
the later call to `handler` will trap into an arbitary address.

We will see the exploits of these two vulnerabilities differ much after we go
further.

## Exploits

We will use two different exploits to attack these two vulnerabilities, namely
the first one is code injection which requires to put the shellcode on an
executable stack, and the second one is return-to-libc attack which does not
need the strict requirement.

### Exploit 1

TODO

exploit-2a.py
exploit-3.py
exploit-4a.py

### Exploit 2

TODO

exploit-2b.py
exploit-4b.py
