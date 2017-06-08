import java.io.*;

class SyntaxError extends Exception {
    SyntaxError(String msg) {
        super(msg);
    }
}

interface Parser {
    void expr() throws IOException, SyntaxError;
    int getLookaheadToken();
    int getTokenCount();
}

class InfixToPostfixTranslator implements Parser {
    private int lookahead;
    private int tokenCount;
    private InputStream input;
    private OutputStream output;

    public InfixToPostfixTranslator(InputStream input, OutputStream output) throws IOException {
        this.input = input;
        this.output = output;
        this.lookahead = input.read();
        this.tokenCount = 0;
    }

    public int getLookaheadToken() {
        return this.lookahead;
    }

    public int getTokenCount() {
        return this.tokenCount;
    }

    public void expr() throws IOException, SyntaxError {
        term();
        while (true) {
            if (this.lookahead == '+') {
                match('+');
                term();
                this.output.write('+');
            } else if (this.lookahead == '-') {
                match('-');
                term();
                this.output.write('-');
            } else break;
        }
    }

    private void term() throws IOException, SyntaxError {
        if (Character.isDigit(this.lookahead)) {
            this.output.write(this.lookahead);
            match(this.lookahead);
        } else {
            throw new SyntaxError(String.format("Expected a digit, got: %c.",
                (char) this.lookahead));
        }
    }

    private void match(int tok) throws IOException, SyntaxError {
        if (this.lookahead == tok) {
            this.lookahead = this.input.read();
            this.tokenCount++;
        } else {
            throw new SyntaxError(String.format("Expected token %c, got: %c.",
                (char) tok, (char) this.lookahead));
        }
    }
}

class InfixToPostfix {
    public static void main(String[] args) throws IOException, SyntaxError {
        OutputStream buffer = new ByteArrayOutputStream();
        Parser translator = new InfixToPostfixTranslator(System.in, buffer);
        try {
            translator.expr();
            System.out.println(buffer.toString());
        } catch (SyntaxError se) {
            System.err.println(String.format(
                "\nSyntax error at token %d: %s",
                translator.getTokenCount(),
                se.getMessage()));
        }
    }
}