#include <stdio.h>
#include <assert.h>
//#include "cpl.h"

#define dprint(expr)    printf(#expr " = %g\n", expr)
#define paste(front, back)  front ## back

void qsort(int v[], int left, int right){
    int i,last;

    if (left>=right)
        return;
    swap(v, left, (left+right)/2);
    last = left;
    for (i=left+1; i<right; i++)
        if(v[i]<v[left])
            swap(v,i,left);
    swap(v, left, last);
    qsort(v, left, last-1);
    qsort(v, last+1, right);
}

void t_qsort(){
    int a[] = {1, 4, 6, 7, 0, 2, 4};
    qsort(a,0, 6);
    int i;
    for (i=0;i<6;i++)
        assert(a[i]<a[i+1]);
}

void t_def(){
    float x,y;
    x=1.0f, y=2.0f;
    dprint(x/y);
    char name1[10];
    paste(name, 1);
}

int main(void){
    t_qsort();
    return 0;
}

