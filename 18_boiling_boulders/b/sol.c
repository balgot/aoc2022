#include "stdio.h"
#include "assert.h"

#define MAX_DIM  30

const int FREE = 0;
const int BLOCK = 1;
const int VISITED = 2;
int cubes[MAX_DIM][MAX_DIM][MAX_DIM];  // initialized to 0


int inside(int x) {
    return 0 <= x && x < MAX_DIM;
}

int all_inside(int x, int y, int z) {
    return inside(x) && inside(y) && inside(z);
}

void dfs(int x, int y, int z, unsigned long long *sides) {
    if (!all_inside(x, y, z)) return;
    if (cubes[x][y][z] == VISITED) return;
    if (cubes[x][y][z] == BLOCK) { (*sides)++; return; }

    cubes[x][y][z] = VISITED;
    for (int nx = x-1; nx <= x+1; ++nx) {
        for (int ny = y-1; ny <= y+1; ++ny) {
            for (int nz = z-1; nz <= z+1; ++nz) {
                int one_set = (nx != x) + (ny != y) + (nz != z) == 1;
                if (one_set) {
                    dfs(nx, ny, nz, sides);
                }
            }
        }
    }
}


int main() {
    int x, y, z;
    while (scanf("%d,%d,%d", &x, &y, &z) != EOF) {
        assert(all_inside(x, y, z));
        cubes[x][y][z] = BLOCK;
    }

    unsigned long long sides = 0;
    for (int i=0; i<MAX_DIM; ++i) {
        for (int j=0; j<MAX_DIM; ++j) {
            dfs(i, j,         0, &sides); // bottom
            dfs(i, j, MAX_DIM-1, &sides); // up

            dfs(i, 0,         j, &sides); // left
            dfs(i, MAX_DIM-1, j, &sides); // right

            dfs(        0, j, i, &sides); // front
            dfs(MAX_DIM-1, j, i, &sides); // back
        }
    }

    printf("%llu", sides);
    return 0;
}