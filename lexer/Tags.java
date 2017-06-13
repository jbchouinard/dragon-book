package lexer;
import java.util.*;
import java.io.*;
public class Tags {
    public static final int
        NUM = 256,
        ID = 257,
        TRUE = 258,
        FALSE = 259,
        OP = 260,
        ASSIGN = 261,
        WHILE = 262,
        FOR = 263,
        DO = 264,
        IF = 265,
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
            case OP: return "OP";
            case ASSIGN: return "ASSIGN";
            case WHILE: return "WHILE";
            case FOR: return "FOR";
            case DO: return "DO";
            case IF: return "IF";
            default: return "INVALID";
        }
    }
}