#include <stdio.h>
#include <string.h>
#include "problem.h"

int main(void) {
    char line[1024];
    while (fgets(line, sizeof line, stdin)) {
        size_t n = strlen(line);
        while (n > 0 && (line[n - 1] == '\n' || line[n - 1] == '\r')) line[--n] = '\0';
        if (n == 0) continue;
        printf("%lld\n", evalPostfix(line));
    }
    return 0;
}
