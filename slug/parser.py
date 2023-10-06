#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from slug.token import Token, TokenType
from slug.expr import Expr, Literal, Grouping, Variable

if TYPE_CHECKING:
    from slug.expr import Expr


class Parser:
    __slots__ = ("tokens", "current")

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current: int = 0

    def peek(self, distance: int = 0) -> Token:
        return self.tokens[self.current + distance]

    def is_at_end(self, distance: int = 0):
        # NOTE: what if distance < 0
        try:
            return self.peek(distance).type == TokenType.EOF
        except IndexError:
            return True

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        else:
            return self.peek().type == token_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.peek(-1)

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()

        raise SyntaxError(f"{message} at {self.peek()}")

    def match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    
    def expression(self) -> "Expr":
        return self.assignment()
    
    def assignment(self) -> "Expr":
        expr: "Expr" = self.or_expression()

        if self.match(TokenType.EQUAL):
            equals: Token = self.peek(-1)
            value: "Expr" = self.assignment()
            
            if isinstance(expr, Variable):
                name: Token = expr.name
                return Assign(name, value)
            elif isinstance(expr, Get):
                return Set(expr.object, expr.name, value)
            
            raise RuntimeError(f"Invalid aassignment target at: {equals}")

        return expr

    def primary(self) -> Expr:
        match self.advance().type:
            case TokenType.FALSE:
                return Literal(False)
            case TokenType.TRUE:
                return Literal(True)
            case TokenType.NONE:
                return Literal(None)
            case TokenType.NUMBER | TokenType.STRING:
                return Literal(self.peek(-1).literal)
            case TokenType.LEFT_PAREN:
                expr: Expr = self.expression()
                self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
                return Grouping(expr)
            case TokenType.IDENTIFIER:
                return Variable(self.peek(-1))
            case _:
                raise SyntaxError(f"Expected expression at: {self.peek()}")   