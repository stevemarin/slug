#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any

from slug.token import Token

class Environment:
    __slots__ = ("values", "enclosing")

    def __init__(self, enclosing: "Environment" | None = None):
        self.values: dict[str, Any] = {}
        self.enclosing = enclosing
    
    def ancestor(self, distance: int) -> "Environment":
        environment: Environment | None = self
        for _ in range(distance):
            if environment is None:
                raise RuntimeError("Enclosing environment is None")
            else:
                environment = environment.enclosing
        
        if environment is None:
            raise RuntimeError("Environment is None")
        
        return environment

    def define(self, name: str, value: Any):
        self.values[name] = value
    
    def _get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        elif self.enclosing is not None:
            return self.enclosing._get(name)
        else:
            raise RuntimeError(f"Undefined variable {name.lexeme} at {name.line}")

    def _get_at(self, distance: int, name: str) -> Any:
        return self.ancestor(distance).values[name]

    def __getitem__(self, name: Token, distance: int | None = None) -> Any:
        if distance is None:
            return self._get(name)
        else:
            return self._get_at(distance, name.lexeme)
    
    def _assign(self, name: Token, value: Any) -> Any:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return value
        elif self.enclosing is not None:
            return self.enclosing._assign(name, value)
        else:
            raise RuntimeError(f"Undefined variable {name.lexeme} at {name.line}")

    def _assign_at(self, name: Token, value: Any, distance: int) -> Any:
        self.ancestor(distance).values[name.lexeme] = value
        return value

    def __setitem__(self, name: Token, value: Any, distance: int | None = None) -> Any:
        if distance is None:
            return self._assign(name, value)
        else:
            return self._assign_at(name, value, distance)