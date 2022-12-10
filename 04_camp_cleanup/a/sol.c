#include <stdio.h>


int main(int argc, char** argv) {
    int contained = 0;
    int a, b, c, d;
    while (scanf("%d-%d,%d-%d", &a, &b, &c, &d) != EOF) {
        if ((c <= a && b <= d) || (a <= c && d <= b)) {
            contained++;
        }
    }
    printf("%d\n", contained);
    return 0;
}
