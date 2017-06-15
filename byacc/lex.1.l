%{
int installID(void);
int installNum(void);

enum tags {
	LT, LE, GT, GE, EQ, NE,
	IF, THEN, ELSE, WHILE, ID, STRING, NUM, RELOP
};

int idCount = 0;
int numCount = 0;
int yylval;
%}

delim		[ \t\n]
ws			{delim}+
letter		[A-Za-z_]
digit		[0-9]
id			{letter}({letter}|{digit})*
number		{digit}+(\.{digit}+)?([Ee][+-]?{digit}+)?
string		\"([^"\\]|\\\"|\\\\)*\"

%%

{ws}		{ /* no action */ }
if			{ return(IF); }
then		{ return(THEN); }
else		{ return(ELSE); }
while		{ return(WHILE); }
{id}		{ yylval = (int) installID(); return(ID); }
{number}	{ yylval = (int) installNum(); return(NUM); }
{string}	{ return(STRING); }
"<"			{ return(LT); }
"<="		{ return(LE); }
">"			{ return(GT); }
">="		{ return(GE); }
"=="		{ return(EQ); }
"!="		{ return(NE); }

%%

const char *get_tag_str(int tag) {
	switch(tag) {
		case LT:
			return "LT";
		case LE:
			return "LE";
		case GT:
			return "GT";
		case GE:
			return "GE";
		case EQ:
			return "EQ";
		case NE:
			return "NE";
		case IF:
			return "IF";
		case THEN:
			return "THEN";
		case ELSE:
			return "ELSE";
		case ID:
			return "ID";
		case NUM:
			return "NUM";
		case STRING:
			return "STRING";
		case RELOP:
			return "RELOP";
		default:
			return "INVALID";
	}
}

int main() {
	int yyret = yylex();
	while (yyret != YY_NULL) {
		printf("<token %s>\n", get_tag_str(yyret));
		yyret = yylex();
	}
}

int installID() {
	return idCount++;
}

int installNum() {
	return numCount++;
}
