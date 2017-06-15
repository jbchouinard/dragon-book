package lexer;
import java.util.*;
import java.io.*;

public class Lex {
    public static void main(String[] args) throws IOException {
        Lexer lex = new Lexer(System.in);
        Token t;
        while ((t = lex.scan()).tag != Tags.STOP) {
            System.out.println(t.toString());
        }
    }
}