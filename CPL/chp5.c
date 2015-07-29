#include <stdio.h>
#include <string.h>
#include "cpl.h"

void swap(int *px, int *py){
    int tmp=*px;
    *px = *py;
    *py = tmp;
}

int Strlen(char *s){
    int n;
    for (n=0; *s != '\0'; s++,n++)
        ;
    return n;
}

#define print_len(s)    printf("len of " #s " is: %d\n", Strlen(s))

#define ALLOCSIZE 10000
static char allocbuf[ALLOCSIZE];
static char *allocp = allocbuf;

char *alloc(int n){
    if(allocbuf + ALLOCSIZE - allocp >=n){
        allocp += n;
        return allocp -n;
    }else{
        return 0;
    }
}

void afree(char *p){
    if (p >= allocbuf && p< allocbuf+ALLOCSIZE)
        allocp = p;
}

int main(void){
    int a[10] = { 1,2,3,4,5,6,7,8,9 };
    swap(a+2, a+3);
    printf("%d\n", a[2]);
    char  *pstr = "abcde";
   print_len(pstr);
    return 0;
}
