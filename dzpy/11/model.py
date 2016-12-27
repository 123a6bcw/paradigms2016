#!/usr/bin/env python3

from operator import (add, sub, mul, floordiv, mod, is_,
                      is_not, lt, gt, le, ge, neg, not_)


class Scope:
    def __init__(self, parent=None):
        self.items = dict()
        self.parent = parent

    def __getitem__(self, item):
        if item in self.items:
            return self.items[item]
        elif self.parent:
            return self.parent.items[item]

    def __setitem__(self, item, value):
        self.items[item] = value


class Number:
    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        ret = Number(0)
        for expr in self.body:
            ret = expr.evaluate(scope)
        return ret


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        ret = Number(0)
        branch = self.if_true
        if not self.condition.evaluate(scope).value:
            branch = self.if_false
        if branch:
            for expr in branch:
                ret = expr.evaluate(scope)
        return ret


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        expr = self.expr.evaluate(scope).value
        print(expr)
        return expr


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        read_Number = Number(int(input()))
        scope[self.name] = read_Number
        return read_Number


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope_items = (arg.evaluate(scope) for arg in self.args)
        call_scope = Scope(scope)
        for name, arg in zip(function.args, call_scope_items):
            call_scope[name] = arg
        return function.evaluate(call_scope)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:
    operations = {"+": add,
                  "-": sub,
                  "*": mul,
                  "/": floordiv,
                  "%": mod,
                  "==": is_,
                  "!=": is_not,
                  "<": lt,
                  ">": gt,
                  "<=": le,
                  ">=": ge,
                  "&&": lambda x, y: x and y,
                  "||": lambda x, y: x or y}

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        lhs = self.lhs.evaluate(scope).value
        rhs = self.rhs.evaluate(scope).value
        return Number(self.operations[self.op](lhs, rhs))


class UnaryOperation:
    operations = {"-": neg,
                  "!": not_}

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        expr = self.expr.evaluate(scope).value
        return Number(self.operations[self.op](expr))


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)


def my_tests():
    global_scope = Scope()
    print("It should print (abs(x) + 1) ^ 2 if abs(x) is odd, else x:")
    print("Write x:", end=' ')
    Read("x").evaluate(global_scope)
    global_scope["foo"] = Function(["a", "b", "c"],
                                   [BinaryOperation(BinaryOperation(
                                                    Reference("a"),
                                                    "+",
                                                    Reference("b")),
                                                    "*",
                                                    Reference("c"))])
    Reference_to_foo = FunctionDefinition("foo", global_scope["foo"])
    global_scope["abs"] = Function(["x"],
                                   [
                                   Conditional(
                                    BinaryOperation(Reference("x"),
                                                    "<",
                                                    Number(0)),
                                    [UnaryOperation("-",
                                                    Reference("x"))],
                                    [Reference("x")])
                                   ])
    Reference_to_abs = FunctionDefinition("abs", global_scope["abs"])

    x = Reference("x").evaluate(global_scope).value

    if abs(x) % 2 == 1:
        print("It should print",
              (abs(Reference("x").evaluate(global_scope).value) + 1) *
              (abs(Reference("x").evaluate(global_scope).value) + 1),
              ": ",
              end=' ')
    else:
        print("It should print", x, ":", end=' ')

    Conditional(
        UnaryOperation("!",
                       BinaryOperation(BinaryOperation(
                                       BinaryOperation(Reference("x"),
                                                       "/",
                                                       Number(2)),
                                       "*",
                                       Number(2)),
                                       "==",
                                       Reference("x"))),
        [
            Print(FunctionCall(Reference_to_foo,
                               [FunctionCall(Reference_to_abs,
                                             [Reference("x")]),
                                Number(1),
                                BinaryOperation(
                                             FunctionCall(Reference_to_abs,
                                                          [Reference("x")]),
                                             "+",
                                             Number(1))]))
        ],
        [
            Print(Reference("x"))
        ]).evaluate(global_scope)


if __name__ == '__main__':
    example()
    my_tests()
