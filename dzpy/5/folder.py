from model import *
from printer import *


class ConstantFolder:
    def __init__(self):
        self.level = 0

    def visit(self, tree):
        return getattr(self, 'visit' + tree.__class__.__name__)(tree)

    def visitNumber(self, Number):
        return Number

    def visitFunction(self, Function):
        for i, expr in enumerate(Function.body):
            Function.body[i] = self.visit(expr)
        return Function

    def visitFunctionDefinition(self, FunctionDefinition):
        FunctionDefinition.function = self.visit(FunctionDefinition.function)
        return FunctionDefinition

    def visitConditional(self, Conditional):
        Conditional.condition = self.visit(Conditional.condition)
        for i, expr in enumerate(Conditional.if_true):
            Conditional.if_true[i] = self.visit(expr)
        if Conditional.if_false:
            for i, expr in enumerate(Conditional.if_false):
                Conditional.if_false[i] = self.visit(expr)
        return Conditional

    def visitPrint(self, Print):
        Print.expr = self.visit(Print.expr)
        return Print

    def visitRead(self, Read):
        return Read

    def visitFunctionCall(self, FunctionCall):
        for i, arg in enumerate(FunctionCall.args):
            FunctionCall.args[i] = self.visit(arg)
        return FunctionCall

    def visitReference(self, Reference):
        return Reference

    def visitBinaryOperation(self, BinaryOperation):
        BinaryOperation.lhs = self.visit(BinaryOperation.lhs)
        BinaryOperation.rhs = self.visit(BinaryOperation.rhs)
        if isinstance(BinaryOperation.lhs,
                      Number) and isinstance(BinaryOperation.rhs,
                                             Number):
            return BinaryOperation.evaluate(...)
        if BinaryOperation.op == '*':
            if isinstance(BinaryOperation.lhs, Number)
            and BinaryOperation.lhs.value == 0
            and isinstance(BinaryOperation.rhs, Reference):
                return Number(0)

            if isinstance(BinaryOperation.lhs, Reference)
            and isinstance(BinaryOperation.rhs, Number)
            and BinaryOperation.rhs.value == 0:
                return Number(0)

        if BinaryOperation.op == '-'
        and isinstance(BinaryOperation.lhs, Reference)
        and isinstance(BinaryOperation.rhs, Reference)
        and BinaryOperation.lhs.name == BinaryOperation.rhs.name:
            return Number(0)

        return BinaryOperation

    def visitUnaryOperation(self, UnaryOperation):
        UnaryOperation.expr = self.visit(UnaryOperation.expr)
        if isinstance(UnaryOperation.expr, Number):
            return UnaryOperation.evaluate(...)
        return UnaryOperation


def folder_my_tests():
    printer = PrettyPrinter()
    folder = ConstantFolder()
    global_scope = Scope()
    printer.visit(folder.visit(Read("x")))
    global_scope["foo"] = Function(["a"],
                                   [BinaryOperation(
                                                    Reference("a"),
                                                    "*",
                                                    Number(0))])
    Reference_to_foo = FunctionDefinition("foo", global_scope["foo"])
    print("\nOld version:")
    printer.visit((FunctionDefinition("foo", global_scope["foo"])))
    print("\nNew version:")
    printer.visit(folder.visit(FunctionDefinition("foo", global_scope["foo"])))
    global_scope["abs"] = Function(["x"],
                                   [
                                   Conditional(
                                    BinaryOperation(Number(0),
                                                    "<",
                                                    Number(0)),
                                    [UnaryOperation("-",
                                                    Number(1))],
                                    [Reference("x")])
                                   ])
    Reference_to_abs = FunctionDefinition("abs", global_scope["abs"])
    print("\nOld version:")
    printer.visit(FunctionDefinition("abs", global_scope["abs"]))
    print("\nNew version:")
    printer.visit(folder.visit(FunctionDefinition("abs", global_scope["abs"])))
    print("\nOld version:")
    printer.visit(Conditional(
        UnaryOperation("!", UnaryOperation("!",
                       BinaryOperation(BinaryOperation(
                                       BinaryOperation(Number(0),
                                                       "*",
                                                       Reference("x")),
                                       "+",
                                       Number(2)),
                                       "==",
                                       BinaryOperation(BinaryOperation(
                                                       Reference("x"),
                                                       "-",
                                                       Reference("x")),
                                                       "+",
                                                       Number(2))))),
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
            Print(BinaryOperation(Reference("x"), "-", Reference("x")))
        ]))

    print("\nNew version:")
    printer.visit(folder.visit(Conditional(
        UnaryOperation("!", UnaryOperation("!",
                       BinaryOperation(BinaryOperation(
                                       BinaryOperation(Number(0),
                                                       "*",
                                                       Reference("x")),
                                       "+",
                                       Number(2)),
                                       "==",
                                       BinaryOperation(BinaryOperation(
                                                       Reference("x"),
                                                       "-",
                                                       Reference("x")),
                                                       "+",
                                                       Number(2))))),
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
            Print(BinaryOperation(Reference("x"), "-", Reference("x")))
        ])))


if __name__ == '__main__':
    folder_my_tests()
