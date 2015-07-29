#include <stdio.h>
#include <assert.h>

void t_enum(void){
    enum months {
        JAN =1,
        FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC
    };
    printf("%d, %d", JAN, MAY);
}

unsigned getbits(unsigned x, int p, int n){
//    printf("%0x\n", ~0);
    return (x>>(p+1-n)) & ~(~0<<n);
}

int bitcount(unsigned x){
    int b;
    for (b=0; x!=0;x>>=1)
        if(x& 01)
            b++;
    return b;
}

int bitcount2(unsigned x){
    int b;
    for (b = 0; x != 0; x &=(x-1),b++) {
    }
    return b;
}
// faster algrithm: MIT HAKMEM

void t_bitcount(){
   int n;
   n = 0xf2;
    assert(5==bitcount(n));
    assert(bitcount(n) == bitcount2(n));
}

int main(void){
//    t_enum();
//    printf("%0x", getbits(n, 6,4));
   t_bitcount();
}
