package lexer;

class Word extends Token {
    public final String lexeme;
    public Word(int t, String lx) {
        super(t); lexeme = new String(lx);
    }
    public String toString() {
        return String.format("<%s, \"%s\">", Tags.toString(tag), lexeme);
    }
}