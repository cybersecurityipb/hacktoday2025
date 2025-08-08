#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void test(char *buf){
    printf(buf);
}

int main(int argc, char** argv){
    char buf[256];
    printf("%p", &buf);
    fgets(buf, 256, stdin);
    test(buf);
    _exit(0);
}

__attribute__((constructor))
void setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}