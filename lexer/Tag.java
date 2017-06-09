package lexer;
import java.util.*;
import java.io.*;
public class Tag {
    public static final int
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
        STOP = (int) Character.MAX_VALUE;
    public static String toString(int tag) {
        if (tag > 0 && tag < 256) {
            return String.format("'%c'", (char) tag);
        }
        switch (tag) {
            case NUM: return "NUM";
            case ID: return "ID";
            case TRUE: return "TRUE";
            case FALSE: return "FALSE";
            case STOP: return "STOP";
            case EQ: return "EQ";
            case NEQ: return "NEQ";
            case LT: return "LT";
            case LTEQ: return "LTEQ";
            case GT: return "GT";
            case GTEQ: return "GTEQ";
            default: return "INVALID";
        }
    }
}