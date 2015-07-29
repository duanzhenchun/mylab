#ifndef _ALL_H
#define _ALL_H
#include <stdio.h>

int readlines(char *lineptr[], int nlines);
void writelines(char *lineptr[], int nlines);

void qsort(void * v[], int left, int right,
        int (*comp)(const void *, const void *));

int numcmp(const char *, const char*);

#endif
