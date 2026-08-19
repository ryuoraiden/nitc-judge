#include <stdio.h>
#include "problem.h"

int main(void) {
    MinHeap h;
    heapInit(&h);

    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'q') break;
        if (cmd == 'i') {
            int key, id;
            if (scanf("%d %d", &key, &id) != 2) break;
            heapInsert(&h, key, id);
            printf("OK\n");
        } else if (cmd == 'x') {
            if (heapEmpty(&h)) printf("EMPTY\n");
            else {
                Item it = heapExtractMin(&h);
                printf("%d %d\n", it.key, it.id);
            }
        } else if (cmd == 'e') {
            printf("%s\n", heapEmpty(&h) ? "YES" : "NO");
        }
    }
    return 0;
}
