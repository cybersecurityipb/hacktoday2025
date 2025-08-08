#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char** argv){
    char buf[256];
    printf("%p", &buf);
    fgets(buf, 256, stdin);
    printf(buf);
    _exit(0);
}

__attribute__((constructor))
void setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

// gcc -fstack-protector-strong -fPIE -pie -Wl,-z,relro -Wl,-z,now chall.c