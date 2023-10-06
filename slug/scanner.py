#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from string import digits, ascii_letters
from typing import Any, Literal

from slug.token import Token, TokenType

DIGITS = frozenset(digits)
LETTERS = frozenset(ascii_letters)


def is_digit(c: str) -> bool:
    return True if c in DIGITS else False


def is_letter(c: str) -> bool:
    return True if c in LETTERS else False


def is_alphanumeric(c: str) -> bool:
    return is_digit(c) or is_letter(c)


class Scanner:
    __slots__ = ("start", "current", "line", "source", "tokens", "length")

    def __init__(self, source: str) -> None:
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

        self.source: str = source
        self.length: int = len(source)
        self.tokens: list[Token] = []
    
    def is_at_end(self, distance: int = 0):
        return self.current + distance >= self.length
    
    def peek(self, distance: int = 0) -> str:
        if self.is_at_end(distance):
            return "\0"
        else:
            return self.source[self.current + distance]
    
    def peek_next_n(self, n: int) -> str:
        return self.source[self.current: self.current + n]

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1: self.current]
    
    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        else:
            self.current += 1
            return True
        
    def current_text(self) -> str:
        return self.source[self.start: self.current]

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

        return self.tokens
    
    def scan_token(self) -> None:
        char: str = self.advance()
        match char:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "/":
                self.add_token(TokenType.SLASH)
            case "!":
                if self.match('='):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
            case '=':
                if self.match('='):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
            case '>':
                if self.match('='):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER)
            case '<':
                if self.match('='):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS)
            case '#':
                if self.match("#"): ## -> ## block comment
                    while self.peek_next_n(2) != "##" and not self.is_at_end():
                        if self.peek() == "\n":
                            self.line += 1
                        self.advance()
                    self.add_token(TokenType.COMMENT, self.current_text())
                    self.current += 2 # skip closing ##
                else: # regular line comment
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                    self.add_token(TokenType.COMMENT, self.current_text())
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case '"' | "'":
                self.string(char)
            case _:
                if is_digit(char):
                    self.number()
                elif is_letter(char):
                    self.identifier()
                else:
                    raise SyntaxError(
                        f"Unexpected character: {char} on line {self.line}"
                    )
            
    def add_token(self, token_type: TokenType, literal: Any = None) -> None:
        self.tokens.append(Token(token_type, self.current_text(), literal, self.line))

    def identifier(self) -> None:
        while is_alphanumeric(self.peek()) or self.peek() == TokenType.UNDERSCORE.value:
            self.advance()

        try:
            token_type: TokenType = TokenType(self.current_text())
        except ValueError:
            token_type = TokenType.IDENTIFIER

        self.add_token(token_type)    
    
    def string(self, quote: Literal["'"] | Literal['"']):
        starting_line = self.line

        while self.peek() != quote and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        
        if self.is_at_end():
            raise SyntaxError(f"Unterminated string on {starting_line}")
        
        # skip the closing quote
        self.advance()

        # drop opening and closing quotes
        literal: str = self.source[self.start + 1: self.current - 1]

        self.add_token(TokenType.STRING, literal)

    def number(self) -> None:
        while is_digit(self.peek()) or self.peek() == TokenType.UNDERSCORE.value:
            self.advance()
        
        if self.peek() == TokenType.DOT.value and is_digit(self.peek(1)):
            self.advance()

            while is_digit(self.peek()) or self.peek() == TokenType.UNDERSCORE.value:
                self.advance()
        
        text: str = self.current_text()
        if TokenType.DOT.value in text:
            self.add_token(TokenType.FLOAT, float(text))
        else:
            self.add_token(TokenType.INTEGER, int(text))


if __name__ == "__main__":
    from textwrap import dedent
    # from pytest import raises

    s = Scanner(dedent("""
        1.23
        -0.76
        +13
        (a * b / dw)
        a = 54
        "iafoieanf
         sinfaeifna
         iefnina"
        class
        ofneaofnaf
        ## 
          this is
          a block comment
        ##
    """))
    s.scan_tokens()

    for t in s.tokens:
        print(t)
