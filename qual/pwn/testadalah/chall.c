#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <unistd.h>
// #include <string.h>

char* TEST[10] = {0};

uint8_t i() {
    uint8_t choice;
    printf("i : ");
    scanf("%hhu", &choice);
    if (choice >= 10) _exit(1);
    return choice;
}

void a(){
    uint8_t idx = i();
    TEST[idx] = malloc(0x40);
    int n = read(0, TEST[idx], 0x40);
    TEST[idx][n - 1] = 0;
}

void b(){
    uint8_t idx = i();
    int x = 0;
    if (TEST[idx] == 0) _exit(1);

    int c = 1;

    while (1) {
        uint8_t val = TEST[idx][x];          
        TEST[idx][x] ^= (rand() & 0xFF);     

        if (val == '\0')                     
            break;

        x++;
    }
}

void c(){
    uint8_t idx = i();
    free(TEST[idx]);
}

void d(){
    uint8_t idx = i();
    printf("%s", TEST[idx]);
}

int main(int argc, char** argv){
    int choice;

    while (1) {
        printf("a - 1, b - 2, c - 3, d - 4: ");
        scanf("%d", &choice);
        switch (choice)
        {
        case 1:
            a();
            break;
        case 2:
            b();
            break;
        case 3:
            c();
            break;
        case 4:
            d();
            break;
        default:
            break;
        }
    }
    _exit(0);
}

void setup() __attribute__((constructor));
void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    uint64_t seed64;
    FILE *urand = fopen("/dev/urandom", "rb");
    if (urand && fread(&seed64, sizeof(seed64), 1, urand) == 1) {
        srand((unsigned int)(seed64 & 0xFFFFFFFF));
    }
    if (urand) fclose(urand);
}