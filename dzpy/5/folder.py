from yat.model import *
from yat.printer import *


class ConstantFolder:
    def __init__(self):
        self.level = 0

    def visit(self, tree):
        return getattr(self, 'visit' + tree.__class__.__name__)(tree)

    def visitNumber(self, Num):
        return Num

    def visitFunction(self, Func):
        for i, expr in enumerate(Func.body):
            Func.body[i] = self.visit(expr)
        return Func

    def visitFunctionDefinition(self, FuncDef):
        FuncDef.function = self.visit(FuncDef.function)
        return FuncDef

    def visitConditional(self, Cond):
        Cond.condition = self.visit(Cond.condition)
        for i, expr in enumerate(Cond.if_true):
            Cond.if_true[i] = self.visit(expr)
        if Cond.if_false is not None:
            for i, expr in enumerate(Cond.if_false):
                Cond.if_false[i] = self.visit(expr)
        return Cond

    def visitPrint(self, P):
        P.expr = self.visit(P.expr)
        return P

    def visitRead(self, R):
        return R

    def visitFunctionCall(self, FuncCall):
        for i, arg in enumerate(FuncCall.args):
            FuncCall.args[i] = self.visit(arg)
        return FuncCall

    def visitReference(self, Ref):
        return Ref

    def visitBinaryOperation(self, BinOp):
        BinOp.lhs = self.visit(BinOp.lhs)
        BinOp.rhs = self.visit(BinOp.rhs)
        if isinstance(BinOp.lhs,
                      Number) and isinstance(BinOp.rhs,
                                             Number):
            return BinOp.evaluate(...)
        if BinOp.op == '*':
            if (isinstance(BinOp.lhs, Number) and
               BinOp.lhs.value == 0 and
               isinstance(BinOp.rhs, Reference)):
                return Number(0)

            if (isinstance(BinOp.lhs, Reference) and
               isinstance(BinOp.rhs, Number) and
               BinOp.rhs.value == 0):
                return Number(0)

        if (BinOp.op == '-' and
           isinstance(BinOp.lhs, Reference) and
           isinstance(BinOp.rhs, Reference) and
           BinOp.lhs.name == BinOp.rhs.name):
            return Number(0)

        return BinOp

    def visitUnaryOperation(self, UnOp):
        UnOp.expr = self.visit(UnOp.expr)
        if isinstance(UnOp.expr, Number):
            return UnOp.evaluate(...)
        return UnOp


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
