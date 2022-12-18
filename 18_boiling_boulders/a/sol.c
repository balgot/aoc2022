#include "stdio.h"
#include "assert.h"

#define MAX_DIM  30
int cubes[MAX_DIM][MAX_DIM][MAX_DIM];  // initialized to 0


int inside(int x) {
    return 0 <= x && x < MAX_DIM;
}


int main() {
    unsigned long long sides = 0;
    int x, y, z;
    while (scanf("%d,%d,%d", &x, &y, &z) != EOF) {
        assert(inside(x));
        assert(inside(y));
        assert(inside(z));

        // if setting the same cube twice, skip
        if (cubes[x][y][z]) {
            continue;
        }

        cubes[x][y][z] = 1;
        sides += 6;

        // check the neighbours
        for (int nx = x-1; nx <= x+1; ++nx) {
            for (int ny = y-1; ny <= y+1; ++ny) {
                for (int nz = z-1; nz <= z+1; ++nz) {
                    int one_set = (nx != x) + (ny != y) + (nz != z) == 1;
                    if (inside(nx) &&
                        inside(ny) &&
                        inside(nz) &&
                        cubes[nx][ny][nz] &&
                        one_set)
                            sides -= 2;
                }
            }
        }
    }

    printf("%llu", sides);
    return 0;
}