#include <stdio.h>


int main(int argc, char** argv) {
    int overlap = 0;
    int a, b, c, d;
    while (scanf("%d-%d,%d-%d", &a, &b, &c, &d) != EOF) {
        if ((c <= a && a <= d) || (a <= c && c <= b)) {
            overlap++;
        }
    }
    printf("%d\n", overlap);
    return 0;
}
