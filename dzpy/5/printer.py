from yat.model import *


class PrettyPrinter:
    tab = "    "

    def __init__(self):
        self.level = 0

    def visit(self, tree, sentence=True):
        if sentence:
            print(self.tab * self.level, end='')
        (getattr(self, 'visit' + tree.__class__.__name__))(tree)
        if sentence:
            print(";")

    def visitNumber(self, NumberObject):
        print(NumberObject.value, end='')

    def visitFunction(self, Func):
        print("(" + ", ".join(Func.args)+")\n" + self.tab*self.level + "{")
        self.level += 1
        for expr in Func.body:
            self.visit(expr, True)
        self.level -= 1
        print(self.tab*self.level + "}", end='')

    def visitFunctionDefinition(self, Func):
        print("def " + Func.name, end='')
        self.visit(Func.function, False)

    def visitConditional(self, Cond):
        print("if (", end='')
        self.visit(Cond.condition, False)
        print(")\n" + self.tab * self.level + "{")
        self.level += 1
        for expr in Cond.if_true:
            self.visit(expr, True)
        self.level -= 1
        if Cond.if_false is not None:
            print(self.tab*self.level + "} else\n" + self.tab*self.level + "{")
            self.level += 1
            for expr in Cond.if_false:
                self.visit(expr, True)
            self.level -= 1
        print(self.tab * self.level + "}", end='')

    def visitPrint(self, P):
        print("print ", end='')
        self.visit(P.expr, False)

    def visitRead(self, R):
        print("read " + R.name, end='')

    def visitFunctionCall(self, FuncCall):
        print(FuncCall.fun_expr.name + "(", end='')
        delimiter = False
        for arg in FuncCall.args:
            if delimiter:
                print(", ", end='')
            else:
                delimiter = True
            self.visit(arg, False)
        print(")", end="")

    def visitReference(self, Ref):
        print(Ref.name, end='')

    def visitBinaryOperation(self, BinOp):
        print("(", end='')
        self.visit(BinOp.lhs, False)
        print(" " + BinOp.op + " ", end='')
        self.visit(BinOp.rhs, False)
        print(")", end='')

    def visitUnaryOperation(self, UnOp):
        print("(" + UnOp.op, end='')
        self.visit(UnOp.expr, False)
        print(")", end='')


def printer_my_tests():
    printer = PrettyPrinter()
    global_scope = Scope()
    printer.visit(Read("x"))
    global_scope["foo"] = Function(["a", "b", "c"],
                                   [BinaryOperation(BinaryOperation(
                                                    Reference("a"),
                                                    "+",
                                                    Reference("b")),
                                                    "*",
                                                    Reference("c"))])
    Reference_to_foo = FunctionDefinition("foo", global_scope["foo"])
    printer.visit(FunctionDefinition("foo", global_scope["foo"]))
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
    printer.visit(FunctionDefinition("abs", global_scope["abs"]))

    printer.visit(Conditional(
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
        ]))


if __name__ == '__main__':
    printer_my_tests()
