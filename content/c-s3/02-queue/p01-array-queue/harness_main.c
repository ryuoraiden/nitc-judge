#include <stdio.h>
#include "problem.h"

int main(void) {
    Queue q;
    initQueue(&q);

    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'q') break;
        if (cmd == 'n') {
            int v;
            if (scanf("%d", &v) != 1) break;
            if (isFull(&q)) printf("FULL\n");
            else { enqueue(&q, v); printf("OK\n"); }
        } else if (cmd == 'd') {
            if (isEmpty(&q)) printf("EMPTY\n");
            else printf("%d\n", dequeue(&q));
        } else if (cmd == 'f') {
            if (isEmpty(&q)) printf("EMPTY\n");
            else printf("%d\n", frontOf(&q));
        } else if (cmd == 'e') {
            printf("%s\n", isEmpty(&q) ? "YES" : "NO");
        }
    }
    return 0;
}
