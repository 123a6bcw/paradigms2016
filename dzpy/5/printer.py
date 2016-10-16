from model import *


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

    def visitNumber(self, Number):
        print(Number.value, end='')

    def visitFunction(self, Function):
        print("(" + ", ".join(Function.args)+")\n" + self.tab*self.level + "{")
        self.level += 1
        for expr in Function.body:
            self.visit(expr, True)
        self.level -= 1
        print(self.tab*self.level + "}", end='')

    def visitFunctionDefinition(self, FunctionDefinition):
        print("def " + FunctionDefinition.name, end='')
        self.visit(FunctionDefinition.function, False)

    def visitConditional(self, Conditional):
        print("if (", end='')
        self.visit(Conditional.condition, False)
        print(")\n" + self.tab * self.level + "{")
        self.level += 1
        for expr in Conditional.if_true:
            self.visit(expr, True)
        self.level -= 1
        if Conditional.if_false:
            print(self.tab*self.level + "} else\n" + self.tab*self.level + "{")
            self.level += 1
            for expr in Conditional.if_false:
                self.visit(expr, True)
            self.level -= 1
        print(self.tab * self.level + "}", end='')

    def visitPrint(self, Print):
        print("print ", end='')
        self.visit(Print.expr, False)

    def visitRead(self, Read):
        print("read " + Read.name, end='')

    def visitFunctionCall(self, FunctionCall):
        print(FunctionCall.fun_expr.name + "(", end='')
        sep = False
        for arg in FunctionCall.args:
            if sep:
                print(", ", end='')
            else:
                sep = True
            self.visit(arg, False)
        print(")", end="")

    def visitReference(self, Reference):
        print(Reference.name, end='')

    def visitBinaryOperation(self, BinaryOperation):
        print("(", end='')
        self.visit(BinaryOperation.lhs, False)
        print(" " + BinaryOperation.op + " ", end='')
        self.visit(BinaryOperation.rhs, False)
        print(")", end='')

    def visitUnaryOperation(self, unop):
        print("(" + unop.op, end='')
        self.visit(unop.expr, False)
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
            Print(Reference("x"))
        ]))


if __name__ == '__main__':
    printer_my_tests()
