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
        reserve(new Word(Tag.TRUE, "true"));
        reserve(new Word(Tag.FALSE, "false"));
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
        // Parse comparison operators
        if (peek == '<') {
            if (peekAhead == '=') {
                read(); read();
                return new Token(Tag.LTEQ);
            } else {
                read();
                return new Token(Tag.LT);
            }
        }
        if (peek == '>') {
            if (peekAhead == '=') {
                read(); read();
                return new Token(Tag.GTEQ);
            } else {
                read();
                return new Token(Tag.GT);
            }
        }
        if (peek == '=') {
            if (peekAhead == '=') {
                read(); read();
                return new Token(Tag.EQ);
            }
        }
        if (peek == '!') {
            if (peekAhead == '=') {
                read(); read();
                return new Token(Tag.NEQ);
            }
        }
        // Parse numbers
        if (Character.isDigit(peek) || peek == '.') {
            StringBuffer buffer = new StringBuffer();
            do {
                buffer.append(peek);
            } while (Character.isDigit(read()) || peek == '.');
            return new Num(Double.parseDouble(buffer.toString()));
        }
        // Parse identifiers and keywords
        if (Character.isLetter(peek)) {
            StringBuffer buffer = new StringBuffer();
            do {
                buffer.append(peek);
            } while (Character.isLetterOrDigit(read()));
            String lexeme = buffer.toString();
            Token token = words.get(lexeme);
            if ((token = words.get(lexeme)) == null) {
                token = new Word(Tag.ID, lexeme);
                words.put(lexeme, token);
            }
            return token;
        }
        if (stop) return new Token(Tag.STOP);
        // Else return generic character token
        Token t = new Token(peek);
        read();
        return t;
    }
}