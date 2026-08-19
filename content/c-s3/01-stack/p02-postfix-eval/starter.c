#include <ctype.h>
#include "problem.h"

long long evalPostfix(const char *expr) {
    Stack s;
    initStack(&s);

    /* TODO: walk the string once.
       - skip spaces
       - a run of digits is one operand: build the number, then push it
       - an operator pops TWO values, combines them, and pushes the result
       Remember the order: the first pop is the RIGHT operand. */

    return 0;
}
