package lexer;

public class Num extends Token {
    public final double value;
    public Num(double v) {
        super(Tag.NUM); value = v;
    }
    public String toString() {
        return String.format("<%s, %f>", Tag.toString(tag), value);
    }
}