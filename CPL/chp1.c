#include <stdio.h>

#define LOWER 0
#define UPPER 300
#define STEP 20

void f_c_temperature(void){
    int fahr;
    for (fahr = LOWER; fahr <= UPPER; fahr += STEP){
        printf ("%3d %6.1f\n", fahr, (5.0/9.0)*(fahr-32));
    }
}

void io(){
    int c;
    while (c=getchar() != EOF){
        putchar(c);
    }
}


#define IN  1
#define OUT 0

void wc(){
    int c, nc, nw, nl, state;

    state=OUT;
    nc=nw=nl=0;
    while(c = getchar()!=EOF){
        ++nc;
        if(c=='\n')
            ++nl;
    }
    printf("words count:%ld, lines count:%d\n", nc, nl);
}

int main(void){
    /* f_c_temperature(); */
    /* io(); */
    char s[]="0";
    printf("%s, %d", s, sizeof(s));
    /* wc(); */
    return 0;
}
