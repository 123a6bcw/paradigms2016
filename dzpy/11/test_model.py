import unittest
from model import *
from io import StringIO
from operator import (add, sub, mul, floordiv, mod, is_,
                      is_not, lt, gt, le, ge, neg, not_)
from unittest.mock import patch


class ScopeTest(unittest.TestCase):
    def test_expected_behaviour(self):
        global_scope = Scope()
        global_scope["test"] = 42
        self.assertEqual(global_scope["test"], 42)


class NumberTest(unittest.TestCase):
    def test_expected_behaviour(self):
        self.scope = Scope()
        test_number = Number(42)
        self.assertIs(test_number.evaluate(self.scope), test_number)


class FunctionTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()

    def test_empty_function_evaluate(self):
        test_func = Function(["Test"], [])
        test_func.evaluate(self.scope)

    def test_function_return_value(self):
        number = Number(100500)
        test_func = Function(["Test"], [Number(322), Number(228), number])
        self.assertIs(test_func.evaluate(self.scope), number)


class FunctionDefinitionTest(unittest.TestCase):
    def test_expected_behaviour(self):
        self.scope = Scope()
        test_function = Function(["arg"], [Number(322), Number(228)])
        test_function_definition = FunctionDefinition("Test",
                                                      test_function)
        self.assertIs(test_function_definition.evaluate(self.scope),
                      test_function)
        self.assertIs(self.scope["Test"], test_function)


class ConditionalTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()

    def test_empty(self):
        Conditional(Number(0), [], []).evaluate(self.scope)
        Conditional(Number(1), [], []).evaluate(self.scope)

    def test_expected_behaviour(self):
        test_true_number = Number(1)
        test_true_conditional = Conditional(Number(1),
                                            [Number(1), test_true_number],
                                            [Number(3)])
        self.assertIs(test_true_conditional.evaluate(self.scope),
                      test_true_number)
        test_false_number = Number(4)
        test_false_conditional = Conditional(Number(0),
                                             [Number(1), test_true_number],
                                             [Number(3), test_false_number])
        self.assertIs(test_false_conditional.evaluate(self.scope),
                      test_false_number)


class PrintTest(unittest.TestCase):
    def test_expected_behaviour(self):
        self.scope = Scope()
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            Print(Number(42)).evaluate(self.scope)
            self.assertEqual(stdout.getvalue(), '42\n')


class ReadTest(unittest.TestCase):
    def test_expected_behaviour(self):
        self.scope = Scope()
        with patch('sys.stdin', new=StringIO('42\n')):
            test_number = Read("Test").evaluate(self.scope)
            self.assertIsInstance(test_number, Number)
            self.assertIs(self.scope["Test"], test_number)


class FunctionCallTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()

    def test_empty_function(self):
        test_function = Function(["arg"], [])
        test_definition = FunctionDefinition("Test", test_function)
        test_call = FunctionCall(test_definition, [Number(42)])
        test_call.evaluate(self.scope)

    def test_expected_behaviour(self):
        test_function = Function(["x", "y"], [Reference("x"), Reference("y")])
        test_definition = FunctionDefinition("func", test_function)
        test_number = Number(42)
        test_call = FunctionCall(test_definition, [Number(1), test_number])
        self.assertIs(test_call.evaluate(self.scope), test_number)


class ReferenceTest(unittest.TestCase):
    def test_reference(self):
        self.scope = Scope()
        self.scope["Test"] = Number(42)
        self.assertIs(Reference("Test").evaluate(self.scope),
                      self.scope["Test"])


class BinaryOperationTest(unittest.TestCase):
    operations = {"+": add,
                  "-": sub,
                  "*": mul,
                  "/": floordiv,
                  "%": mod}

    logic_operations = {"==": is_,
                        "!=": is_not,
                        "<": lt,
                        ">": gt,
                        "<=": le,
                        ">=": ge,
                        "&&": lambda x, y: x and y,
                        "||": lambda x, y: x or y}

    def setUp(self):
        self.scope = Scope()

    def test_expected_arithmetic_result(self):
        test_lhs = 42
        test_rhs = 322
        for test_operation, test_function in self.operations.items():
            test_result = BinaryOperation(
                                         Number(test_lhs),
                                         test_operation,
                                         Number(test_rhs)).evaluate(self.scope)
            self.assertEqual(test_function(test_lhs, test_rhs),
                             test_result.value)

    def test_expected_logic_result(self):
        test_lhs = 42
        test_rhs = 322
        for test_operation, test_function in self.logic_operations.items():
            test_result = BinaryOperation(
                                         Number(test_lhs),
                                         test_operation,
                                         Number(test_rhs)).evaluate(self.scope)
            if (test_function(test_lhs, test_rhs)):
                self.assertTrue(test_result.value)
            else:
                self.assertFalse(test_result.value)


class UnaryOperationTest(unittest.TestCase):
    def setUp(self):
        self.scope = Scope()

    def test_expected_neg_result(self):
        test_value = 42
        test_result = UnaryOperation("-",
                                     Number(test_value)).evaluate(self.scope)
        self.assertEqual(test_result.value, neg(test_value))

    def test_expected_not_result(self):
        test_value = 42
        test_result = UnaryOperation("!",
                                     Number(test_value)).evaluate(self.scope)
        self.assertEqual(test_result.value, not_(test_result))


if __name__ == '__main__':
    unittest.main()
