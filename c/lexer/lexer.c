#include <stdlib.h>
#include <stdio.h>

enum tag_t {
    NUM = 256,
    ID = 257,
    TRUE = 258,
    FALSE = 259,
    EQ = 260,
    NEQ = 261,
    LT = 262,
    LTEQ = 263,
    GT = 264,
    GTEQ = 265,
    STOP = -1,
};

typedef enum tag_t tag;

struct token_t {
    tag tag;
    union {
        long integer;
        double decimal;
        char* string;
    } val;
};

typedef struct token_t token;

int main(int argc, char* argv[]) {
    token *t = malloc(sizeof(token));
    free((void*) t);
    return 0;
}