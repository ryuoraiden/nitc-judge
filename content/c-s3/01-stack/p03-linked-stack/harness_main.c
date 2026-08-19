#include <stdio.h>
#include "problem.h"

int main(void) {
    STACK s = SINIT();

    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'q') break;
        if (cmd == 'p') {
            int v;
            if (scanf("%d", &v) != 1) break;
            s = PUSH(s, v);
        } else if (cmd == 'o') {
            if (ISEMPTY(s)) printf("EMPTY\n");
            else { printf("%d\n", TOP(s)); s = POP(s); }
        } else if (cmd == 't') {
            if (ISEMPTY(s)) printf("EMPTY\n");
            else printf("%d\n", TOP(s));
        } else if (cmd == 'd') {
            SPRNT2B(s);
        }
    }
    return 0;
}
