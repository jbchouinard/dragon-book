package lexer;

public class Num extends Token {
    public final double value;
    public Num(double v) {
        super(Tags.NUM); value = v;
    }
    public String toString() {
        return String.format("<%s, %f>", Tags.toString(tag), value);
    }
}