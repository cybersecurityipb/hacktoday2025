#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

const unsigned char lookup_table[256] = {
    234, 9, 103, 60, 5, 79, 232, 229, 45, 51, 131, 3, 168, 29, 170, 216,
    99, 161, 111, 204, 220, 209, 78, 89, 72, 191, 157, 119, 226, 184, 244, 134,
    21, 61, 175, 15, 223, 100, 230, 28, 128, 185, 84, 208, 164, 44, 113, 105,
    27, 85, 203, 146, 153, 130, 66, 42, 250, 140, 174, 133, 115, 4, 52, 73,
    65, 10, 104, 238, 30, 211, 46, 121, 2, 190, 159, 172, 112, 156, 95, 47,
    124, 177, 77, 202, 81, 38, 123, 13, 182, 242, 64, 33, 225, 0, 241, 122,
    210, 37, 106, 163, 82, 98, 34, 218, 187, 214, 125, 132, 120, 219, 252, 32,
    135, 215, 245, 48, 198, 222, 76, 231, 213, 192, 227, 144, 19, 152, 110, 12,
    217, 126, 196, 201, 248, 148, 109, 138, 63, 249, 200, 36, 197, 101, 127, 145,
    149, 54, 16, 167, 102, 80, 239, 181, 14, 83, 224, 142, 69, 176, 118, 171,
    251, 136, 43, 246, 155, 18, 165, 68, 53, 90, 94, 41, 93, 162, 116, 212,
    205, 25, 235, 193, 74, 58, 169, 199, 17, 180, 49, 147, 92, 158, 160, 75,
    141, 20, 96, 31, 137, 117, 186, 11, 67, 233, 88, 91, 24, 97, 237, 247,
    86, 195, 236, 39, 221, 87, 240, 178, 40, 206, 194, 1, 207, 71, 150, 114,
    56, 107, 243, 179, 166, 183, 50, 143, 254, 154, 129, 59, 55, 23, 7, 8,
    108, 151, 22, 139, 228, 253, 173, 26, 188, 35, 255, 62, 70, 189, 6, 57};

int f0(uint8_t x) { return ((x ^ 0x4F) + 3) == 0x51; }
int f1(uint8_t x) { return ((~x + 7) & 0xFF) == 0x68; }
int f2(uint8_t x) { return ((x + 5) ^ 0xAA) == 0x28; }
int f3(uint8_t x) { return (((x << 1) - 10) & 0xFF) == 0xFC; }
int f4(uint8_t x) { return ((x & 0xF0) | (x >> 4)) == 0x66; }
int f5(uint8_t x) { return (((x ^ 0x3C) + 0x10) & 0xFF) == 0x5F; }
int f6(uint8_t x) { return (x - 0x20) == 0x70; }
int f7(uint8_t x) { return ((x ^ (x << 1)) & 0xFF) == 0x12; }
int f8(uint8_t x) { return (((x * 2) ^ 0x33) & 0xFF) == 0x65; }
int f9(uint8_t x) { return (((x >> 2) + 0x55) & 0xFF) == 0x87; }
int f10(uint8_t x) { return (x ^ 0xAB) == 0x43; }
int f11(uint8_t x) { return (~(x - 3) & 0xFF) == 0x56; }
int f12(uint8_t x) { return ((x ^ 0x12) + 0x01) == 0xA0; }
int f13(uint8_t x) { return (((x << 2) ^ 0xA5) & 0xFF) == 0x29; }
int f14(uint8_t x) { return ((x + 0x55) ^ 0xAA) == 0x69; }
int f15(uint8_t x) { return ((~x + 0x10) & 0xFF) == 0x11; }
int f16(uint8_t x) { return (x ^ 0xFF) == 0xFF; }
int f17(uint8_t x) { return (((x * 3) - 7) & 0xFF) == 0x2E; }
int f18(uint8_t x) { return ((x >> 1) + 0x33) == 0x9B; }
int f19(uint8_t x) { return ((x ^ (x << 1)) & 0xFF) == 0xF9; }
int f20(uint8_t x) { return (((x + 0x22) ^ 0x77) & 0xFF) == 0x11; }
int f21(uint8_t x) { return ((x ^ 0x12) + 0x20) == 0x64; }
int f22(uint8_t x) { return ((x * 3 + 1) & 0xFF) == 0x2B; }
int f23(uint8_t x) { return ((x + 0x3A) ^ 0x5F) == 0xB3; }
int f24(uint8_t x) { return (((x ^ 0x3C) - 0x22) & 0xFF) == 0xBD; }
int f25(uint8_t x) { return ((x * 3 + 5) & 0xFF) == 0xA0; }
int f26(uint8_t x) { return (((x >> 2) + 0x33) & 0xFF) == 0x4F; }
int f27(uint8_t x) { return (((x ^ (x << 1)) + 7) & 0xFF) == 0x79; }
int f28(uint8_t x) { return ((~(x ^ 0xB2) + 0x2A) & 0xFF) == 0xD4; }
int f29(uint8_t x) { return (((x + 0xA6) ^ 0x5A) & 0xFF) == 0xA5; }
int f30(uint8_t x) { return (((x ^ 0x32) + 0x10) & 0xFF) == 0xB5; }
int f31(uint8_t x) { return ((~x + 0x20) & 0xFF) == 0x1E; }
int f32(uint8_t x) { return ((x ^ 0xAA) + 3) == 0x32; }
int f33(uint8_t x) { return ((x + 0x10) ^ 0xD6) == 0x00; }
int f34(uint8_t x) { return (((x ^ 0x3C) - 0x22) & 0xFF) == 0xD2; }
int f35(uint8_t x) { return ((x * 3 + 5) & 0xFF) == 0x3D; }
int f36(uint8_t x) { return (((x >> 2) + 0x33) & 0xFF) == 0x4D; }
int f37(uint8_t x) { return (((x ^ (x << 1)) + 7) & 0xFF) == 0x6D; }
int f38(uint8_t x) { return ((~(x ^ 0x48) + 0x2A) & 0xFF) == 0xD4; }
int f39(uint8_t x) { return (((x + 0xC9) ^ 0x5A) & 0xFF) == 0xA5; }
int f40(uint8_t x) { return (((x ^ 0x87) + 0x10) & 0xFF) == 0xB5; }
int f41(uint8_t x) { return ((~x + 0x20) & 0xFF) == 0x9F; }
int f42(uint8_t x) { return ((x ^ 0xDE) - 3) == 0x45; }
int f43(uint8_t x) { return ((x ^ 0xB0) + 0x12) == 0x76; }
int f44(uint8_t x) { return (x ^ 0x77) == 0x55; }
int f45(uint8_t x) { return ((x + 0xb0) & 0xFF) == 0x23; }
int f46(uint8_t x) { return ((x * 2) & 0xFF) == 0xDA; }
int f47(uint8_t x) { return ((x ^ 0x4b) + 0x11) == 0x11; }
int f48(uint8_t x) { return ((x >> 1) + 0x10) == 0x8A; }
int f49(uint8_t x) { return (x ^ 0x5c) == 0x55; }
int f50(uint8_t x) { return ((x ^ 0x23) + 0x55) == 0xB8; }
int f51(uint8_t x) { return ((x * 2) & 0xFF) == 0x16; }
int f52(uint8_t x)
{
    uint8_t rotated = ((x << 1) | (x >> 7)) & 0xFF;
    return (rotated ^ 0x5A) == 0xB1;
}
int f53(uint8_t x)
{
    uint8_t swapped = ((x & 0x0F) << 4) | ((x & 0xF0) >> 4);
    return (swapped + 0x44) == 0x6B;
}
int f54(uint8_t x)
{
    uint8_t temp = (x * 3) & 0xFF;
    return (temp ^ 0x3C) == 0xAB;
}
int f55(uint8_t x) { return ((~x + 0x77) & 0xFF) == 0x07; }
int f56(uint8_t x) { return (((x << 2) ^ 0x49) & 0xFF) == 0xDD; }
int f57(uint8_t x) { return ((x ^ 0xd1) + 0x11) == 0x11; }
int f58(uint8_t x) { return ((x >> 1) + 0x88) == 0xC5; }
int f59(uint8_t x) { return (x ^ 0x2f) == 0x55; }
int f60(uint8_t x) { return (((x * 5) ^ 0x66) & 0xFF) == 0x5D; }
int f61(uint8_t x) { return (((x >> 3) ^ 0x42) + 0x31) == 0x8E; }
int f62(uint8_t x) { return ((x + 0x29) ^ 0x77) == 0x9D; }
int f63(uint8_t x) { return ((x >> 1) + 0x10) == 0x88; }
int f64(uint8_t x) { return (((x ^ 0x31) * 2) & 0xFF) == 0x2A; }
int f65(uint8_t x) { return ((~x + 0x29) & 0xFF) == 0x68; }
int f66(uint8_t x) { return (((x << 1) ^ 0x8F) & 0xFF) == 0x85; }
int f67(uint8_t x)
{
    uint8_t swapped = ((x & 0x0F) << 4) | ((x & 0xF0) >> 4);
    return (swapped - 0x15) == 0x78;
}
int f68(uint8_t x) { return (((x * 3) ^ 0x2A) & 0xFF) == 0x63; }
int f69(uint8_t x)
{
    uint8_t rotated = ((x >> 3) | (x << 5)) & 0xFF;
    return (rotated + 0x17) == 0xB7;
}
int f70(uint8_t x) { return (((x ^ 0x55) * 2) & 0xFF) == 0xCC; }
int f71(uint8_t x) { return ((x >> 2) + 0x88) == 0xC5; }
int f72(uint8_t x)
{
    uint8_t count = __builtin_popcount(x);
    return ((x + count) ^ 0x4C) == 0xD7;
}
int f73(uint8_t x) { return ((x & 0xF0) | 0x07) == 0x67; }
int f74(uint8_t x) { return (((x << 3) ^ 0x33) & 0xFF) == 0xC3; }
int f75(uint8_t x)
{
    uint8_t rev = 0;
    for (int i = 0; i < 8; i++)
    {
        rev |= ((x >> i) & 1) << (7 - i);
    }
    return (rev + 0x2B) == 0xD0;
}
int f76(uint8_t x) { return ((x >> 2) ^ 0x71) == 0x5E; }
int f77(uint8_t x) { return ((x ^ 0xAA) + 0x38) == 0x87; }
int f78(uint8_t x) { return (((x * 5) ^ 0x64) & 0xFF) == 0x5A; }
int f79(uint8_t x)
{
    uint8_t rotated = ((x << 2) | (x >> 6)) & 0xFF;
    return (rotated - 0x45) == 0x85;
}
int f80(uint8_t x) { return ((~x + 0x77) & 0xFF) == 0xB7; }
int f81(uint8_t x) { return (((x << 1) ^ 0x29) & 0xFF) == 0x9F; }
int f82(uint8_t x)
{
    uint8_t nibble_sum = (x >> 4) + (x & 0x0F);
    return (x + nibble_sum) == 0xCE;
}
int f83(uint8_t x) { return (((x * 7) ^ 0x42) & 0xFF) == 0x32; }
int f84(uint8_t x) { return ((x >> 1) + 0x99) == 0xBD; }
int f85(uint8_t x) { return ((((x << 3) & 0xFF) >> 2) - 0x1A) == 0x1C; }

int (*checks[])(uint8_t) = {
    f0, f1, f2, f3, f4, f5, f6, f7, f8, f9,
    f10, f11, f12, f13, f14, f15, f16, f17, f18, f19,
    f20, f21, f22, f23, f24, f25, f26, f27, f28, f29,
    f30, f31, f32, f33, f34, f35, f36, f37, f38, f39,
    f40, f41, f42, f43, f44, f45, f46, f47, f48, f49,
    f50, f51, f52, f53, f54, f55, f56, f57, f58, f59,
    f60, f61, f62, f63, f64, f65, f66, f67, f68, f69,
    f70, f71, f72, f73, f74, f75, f76, f77, f78, f79,
    f80, f81, f82, f83, f84, f85};

unsigned char shift(char c, int position)
{
    int shifts = (position * 5 + 3) % 94;
    return ((c - 32 + shifts) % 94) + 32;
}

unsigned char rot13(unsigned char c)
{
    if (c >= 'a' && c <= 'z')
        return (c - 'a' + 13) % 26 + 'a';
    if (c >= 'A' && c <= 'Z')
        return (c - 'A' + 13) % 26 + 'A';
    return c;
}

unsigned char rol(unsigned char b, int bits)
{
    return ((b << bits) | (b >> (8 - bits))) & 0xFF;
}

unsigned char keyxor(unsigned char b, int position)
{
    unsigned char key = (position * 7 + 11) % 256;
    return b ^ key;
}

unsigned char lookup(unsigned char b)
{
    return lookup_table[b];
}

unsigned char not(unsigned char b)
{
    return ~b & 0xFF;
}

unsigned char addpos(unsigned char b, int position)
{
    return (b + (position % 17)) % 256;
}

unsigned char swap_nibble(unsigned char b)
{
    return ((b & 0x0F) << 4) | ((b & 0xF0) >> 4);
}

unsigned char xor_a5(unsigned char b)
{
    return b ^ 0xA5;
}

unsigned char rol3(unsigned char b)
{
    return rol(b, 3);
}

unsigned char xor3c(unsigned char b)
{
    return b ^ 0x3C;
}

unsigned char rol1(unsigned char b)
{
    return rol(b, 1);
}

unsigned char full_transform(char input, int position)
{
    unsigned char c1 = shift(input, position);
    unsigned char c2 = rot13(c1);
    unsigned char c3 = rol(c2, position % 8);
    unsigned char c4 = keyxor(c3, position);
    unsigned char c5 = lookup(c4);
    unsigned char c6 = not(c5);
    unsigned char c7 = addpos(c6, position);
    unsigned char c8 = swap_nibble(c7);
    unsigned char c9 = xor_a5(c8);
    unsigned char c10 = rol3(c9);
    unsigned char c11 = xor3c(c10);
    unsigned char c12 = rol1(c11);
    return c12;
}

int verify_flag(const char *input)
{
    size_t len = strlen(input);
    if (len != 86)
        return 0;

    for (int i = 0; i < len; i++)
    {
        unsigned char transformed = full_transform(input[i], i + 1);
        if (!checks[i](transformed))
        {
            return 0;
        }
    }
    return 1;
}

int main()
{
    char input[128];
    printf("Enter the flag: ");
    if (fgets(input, sizeof(input), stdin) == NULL)
        return 1;
    input[strcspn(input, "\n")] = '\0';

    if (verify_flag(input))
    {
        puts("✅ Correct flag!");
    }
    else
    {
        puts("❌ Incorrect flag.");
    }
    return 0;
}
