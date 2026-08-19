#include <ctype.h>
#include "problem.h"

long long evalPostfix(const char *expr) {
    Stack s;
    initStack(&s);

    for (const char *p = expr; *p != '\0'; ) {
        if (*p == ' ') { p++; continue; }

        if (isdigit((unsigned char)*p)) {
            long long value = 0;
            while (isdigit((unsigned char)*p)) {
                value = value * 10 + (*p - '0');
                p++;
            }
            push(&s, value);
        } else {
            char op = *p++;
            long long right = pop(&s);      /* first pop is the right operand */
            long long left  = pop(&s);
            long long result = 0;
            switch (op) {
                case '+': result = left + right; break;
                case '-': result = left - right; break;
                case '*': result = left * right; break;
                case '/': result = (right != 0) ? left / right : 0; break;
                default:  result = 0; break;
            }
            push(&s, result);
        }
    }

    return isEmpty(&s) ? 0 : pop(&s);
}
