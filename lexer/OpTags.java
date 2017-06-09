package lexer;
public class OpTags {
    public static final int
        EQ = 1,
        NEQ = 2,
        LT = 3,
        LTEQ = 4,
        GT = 5,
        GTEQ = 6,
        ADD = 7,
        SUB = 8,
        MUL = 9,
        DIV = 10;
    public static String toString(int op) {
        switch (op) {
            case EQ: return "==";
            case NEQ: return "!=";
            case LT: return "<";
            case LTEQ: return "<=";
            case GT: return ">";
            case GTEQ: return ">=";
            case ADD: return "+";
            case SUB: return "-";
            case MUL: return "*";
            case DIV: return "/";
            default: return "INVALID";
        }
    }
}