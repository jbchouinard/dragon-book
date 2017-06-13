%{
#include <stdio.h>
%}

ws      [ \t]*
char    [^ \t]

%%

{ws}    { putchar(' '); }
{char}  { putchar(*yytext); }

%%

int main() {
    yylex();
}
