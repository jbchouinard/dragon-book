package lexer;
import java.util.*;
import java.io.*;

public class Lexer {
    public int line = 1;
    public int col = 1;
    private char peek = ' ';
    private char peekAhead = ' ';
    private boolean stop = false;
    private Hashtable<String, Token> words = new Hashtable<String, Token>();
    private final InputStream input;

    void reserve(Word w) {
        words.put(w.lexeme, w);
    }
    char read() throws IOException {
        col++;
        int next = input.read();
        if (next == -1) stop = true;
        peek = peekAhead;
        peekAhead = (char) next;
        if (peek == '\n') { col = 1; line++; }
        return peek;
    }
    public Lexer(InputStream in) throws IOException {
        input = in;
        peekAhead = (char) in.read();
        reserve(new Word(Tags.TRUE, "true"));
        reserve(new Word(Tags.FALSE, "false"));
        reserve(new Word(Tags.WHILE, "while"));
        reserve(new Word(Tags.FOR, "for"));
        reserve(new Word(Tags.DO, "do"));
        reserve (new Word(Tags.IF, "if"));
    }
    public Token scan() throws IOException {
        // Skip whitespace and comments
        while (peek == ' ' || peek == '\t' || peek == '\n' || peek == '/') {
            if (peek == '/') {
                if (peekAhead == '/') {
                    while (peek != '\n' && !stop) read();
                } else if (peekAhead == '*') {
                    while (!(peek == '*' && peekAhead == '/') && !stop) read();
                    read();
                } else break;;
            }
            read();
        }
        // Read operators
        switch (peek) {
            case '<':
                if (peekAhead == '=') {
                    read(); read();
                    return new Op(OpTags.LTEQ);
                } else {
                    read();
                    return new Op(OpTags.LT);
                }
            case '>':
                if (peekAhead == '=') {
                    read(); read();
                    return new Op(OpTags.GTEQ);
                } else {
                    read();
                    return new Op(OpTags.GT);
                }
            case '=':
                if (peekAhead == '=') {
                    read(); read();
                    return new Op(OpTags.EQ);
                }
                else {
                    read();
                    return new Token(Tags.ASSIGN);
                }
            case '!':
                if (peekAhead == '=') {
                    read(); read();
                    return new Op(OpTags.NEQ);
                } else break;
            case '+':
                read();
                return new Op(OpTags.ADD);
            case '-':
                read();
                return new Op(OpTags.SUB);
            case '*':
                read();
                return new Op(OpTags.MUL);
            case '/':
                read();
                return new Op(OpTags.DIV);
            case '&':
                if (peekAhead == '&') {
                    read(); read();
                    return new Op(OpTags.AND);
                } else break;
            case '|':
                if (peekAhead == '|') {
                    read(); read();
                    return new Op(OpTags.OR);
                } else break;
            default:
                break;
        }
        // Read numbers
        if (Character.isDigit(peek) || peek == '.') {
            StringBuffer buffer = new StringBuffer();
            do {
                buffer.append(peek);
            } while (Character.isDigit(read()) || peek == '.');
            return new Num(Double.parseDouble(buffer.toString()));
        }
        // Read identifiers and keywords
        if (Character.isLetter(peek)) {
            StringBuffer buffer = new StringBuffer();
            do {
                buffer.append(peek);
            } while (Character.isLetterOrDigit(read()));
            String lexeme = buffer.toString();
            Token token = words.get(lexeme);
            if ((token = words.get(lexeme)) == null) {
                token = new Word(Tags.ID, lexeme);
                words.put(lexeme, token);
            }
            return token;
        }
        // Check if reached end of input
        if (stop) return new Token(Tag.STOP);
        // Else return generic character token
        Token t = new Token(peek);
        read();
        return t;
    }
}