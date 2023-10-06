#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from slug.environment import Environment

if TYPE_CHECKING:
    from slug.expr import Expr
    # from slug.stmt import Stmt

class Interpreter:
    __slots__ = ("globals", "locals", "environment")

    def __init__(self) -> None:
        self.globals: Environment = Environment()
        self.environment = self.globals
        self.locals: dict["Expr", int] = {}
    
    def resolve(self, expr: "Expr", depth: int) -> None:
        self.locals[expr] = depth
    
    @staticmethod
    def interpret(statements: list["Stmt"]) -> None:
        for statement in statements:
            statement.evaluate()

interpreter = Interpreter()