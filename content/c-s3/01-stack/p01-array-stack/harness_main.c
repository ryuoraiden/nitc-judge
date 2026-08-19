#include <stdio.h>
#include "problem.h"

int main(void) {
    Stack s;
    initStack(&s);

    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'q') break;
        if (cmd == 'p') {
            int v;
            if (scanf("%d", &v) != 1) break;
            if (isFull(&s)) printf("FULL\n");
            else { push(&s, v); printf("OK\n"); }
        } else if (cmd == 'o') {
            if (isEmpty(&s)) printf("EMPTY\n");
            else printf("%d\n", pop(&s));
        } else if (cmd == 'k') {
            if (isEmpty(&s)) printf("EMPTY\n");
            else printf("%d\n", peek(&s));
        } else if (cmd == 'e') {
            printf("%s\n", isEmpty(&s) ? "YES" : "NO");
        }
    }
    return 0;
}
