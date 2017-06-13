package lexer;
public class Op extends Token {
    private final int optag;
    public Op(int op) {
        super(Tags.OP);
        optag = op;
    }
    public String toString() {
        return String.format("<%s, '%s'>", Tags.toString(tag), OpTags.toString(optag));
    }
}