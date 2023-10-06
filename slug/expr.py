#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Any, TYPE_CHECKING

from slug.token import Token

if TYPE_CHECKING:
    from slug.interpreter import Interpreter


class Expr(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self) -> None:
        ...
    
    @abstractmethod
    def __repr__(self) -> str:
        ...
    
    @abstractmethod
    def evaluate(self) -> Any:
        ...
    
    # @abstractmethod
    # def resolve(self, resolver: "Rsolver") -> None:
    #     ...


class Literal(Expr):
    __slots__ = ("value")

    def __init__(self, value: Any) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"(Literal {str(self.value)})"

    def evaluate(self) -> Any:
        return self.value

    # def resolve(self, resolver: "Resolver") -> None:
    #     return None


class Grouping(Expr):
    __slots__ = ("expression")

    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def __repr__(self) -> str:
        return f"(Group {self.expression})"

    def evaluate(self) -> Any:
        return self.expression.evaluate()

    # def resolve(self, resolver: "Resolver") -> None:
    #     self.expression.resolve(resolver)


class Variable(Expr):
    __slots__ = ("name")

    def __init__(self, name: Token):
        self.name = name
    
    def __repr__(self):
        return f"(Variable {self.name})"
    
    def evaluate(self) -> Any:
        return self.lookup_variable(self.name, self)
    
    def get_distance(self, expr: "Expr", interpreter: "Interpreter") -> int:
        distance: int | None = interpreter.locals[expr]
        if distance is None:
            raise RuntimeError(f"Cannot find expr: {expr}")
        else:
            return distance

    def lookup_variable(self, name: Token, expr: Expr) -> Any:
        from slug.interpreter import interpreter

        try:
            distance = self.get_distance(expr, interpreter)
            return interpreter.environment.__getitem__(name, distance)
        except KeyError:
            return interpreter.globals[name]
 