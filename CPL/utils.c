#include <stdlib.h>
#include "cpl.h"

void swap(void *v[], int i, int j){
    void *tmp;
    tmp = v[i];
    v[i] = v[j];
    v[j] = tmp;
}

void qsort(void *v[], int left, int right, int (*comp)(const void *, const void *)){
    int i,last;

    if (left>=right)
        return;
    swap(v, left, (left+right)/2);
    last = left;
    for (i=left+1; i<right; i++)
        if((*comp)(v[i],v[left]) < 0)
            swap(v,i,left);
    swap(v, left, last);
    qsort(v, left, last-1, comp);
    qsort(v, last+1, right, comp);

}

int numcmp(const char *s1, const char *s2){
    double v1,v2;
    v1=atof(s1);
    v2=atof(s2);
    if (v1<v2)
        return -1;
    else if (v1>v2)
        return 1;
    else
        return 0;
}
