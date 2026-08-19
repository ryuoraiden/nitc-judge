#include <stdio.h>
#include "problem.h"

int main(void) {
    QUEUE q = QINIT();

    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'q') break;
        if (cmd == 'n') {
            int v;
            if (scanf("%d", &v) != 1) break;
            q = ENQUEUE(q, v);
            printf("OK\n");
        } else if (cmd == 'd') {
            if (ISEMPTYQUEUE(q)) printf("EMPTY\n");
            else { printf("%d\n", FRONT(q)); q = DEQUEUE(q); }
        } else if (cmd == 'f') {
            if (ISEMPTYQUEUE(q)) printf("EMPTY\n");
            else printf("%d\n", FRONT(q));
        } else if (cmd == 'e') {
            printf("%s\n", ISEMPTYQUEUE(q) ? "YES" : "NO");
        }
    }
    return 0;
}
