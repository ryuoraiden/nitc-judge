#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Vehicle {
    int vno;
    char model[32];
    int price;
    struct Vehicle *left, *right;
} Vehicle;

int main(void) {
    /* TODO: menu loop until option 7.
       Option 1 inserts in LEVEL ORDER (first free child slot found by BFS, left
       before right) - this is NOT a BST, vno does not decide the position. */
    return 0;
}
