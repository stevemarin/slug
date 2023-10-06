#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from typing import Any

class TokenType(Enum):
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COMMA = ","
    DOT = "."
    MINUS = "-"  
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"
    UNDERSCORE = "_"
    POUND = "#"

    BANG = "!"
    BANG_EQUAL = "!="
    EQUAL = "="
    EQUAL_EQUAL = "=="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="

    AND = "and"
    NOT = "not"
    STRUCT = "struct"
    CLASS = "class"
    ELSE = "else"
    FALSE = "Talse"
    FUN = "fun"
    FOR = "for"
    IF = "if"
    NIL = "nil"
    NONE = "None"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "True"
    VAR = "var"
    WHILE = "while"

    IDENTIFIER = "identifier"
    STRING = "str"
    NUMBER = "number"
    INTEGER = "int"
    FLOAT = "float"
    COMMENT = "comment"

    EOF = "eof"


class Token:
    __slots__ = ("type", "lexeme", "literal", "line")

    def __init__(self, type: TokenType, lexeme: str, literal: Any, line: int):
        self.type: TokenType = type
        self.lexeme: str = lexeme
        self.literal: Any = literal
        self.line: int = line

    def __repr__(self):
        return f"{self.type} {self.lexeme} {self.literal}"
