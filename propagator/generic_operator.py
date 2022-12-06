"""
Support for generic operatiors.

This module contains functions to make generic operators and to assign a
function to this operator if the operator's arguments match given function
tests.

How to use this module
----------------------

>>> from propagator.generic_operator import make_generic_operator,assign_operation
>>> concat = make_generic_operator(2, "concat", lambda x, y: x + y)
>>> concat("hello ", "world")
hello world
>>> is_number = lambda x: isinstance(x, (int, float, complex))
>>> concat_numbers = lambda x, y: str(x) + str(y)
>>> assign_operation("concat", concat_numbers, (is_number, is_number))
>>> concat(1, 2)
12
"""

from collections import deque
from collections.abc import Iterable
from propagator.logging import debug

generic_operators = {}

"""
Calls one of assigned operators according to the types of its arguments.
"""
class _GenericOperator:
    """
    Initialize a `_GenericOperator` with a default operation and no
    assigned functions.

    Parameters:

    - arity: the number of arguments of the operator
    - default_function: the function that will be called if there are no
      assigned operators.
    """
    def __init__(self, name, arity, default_function):
        self.name = name
        self.arity = arity
        self.default_function = default_function
        self.assigned_operations = deque()

    def operator_for(self, *args):
        def matches(things, tests):
            return all(test(thing) for thing, test in zip(things, tests))

        assert len(args) == self.arity, \
            "Expected arity {0}, received {1}\nArgs: {2}".format(self.arity, len(args), args)

        for op in self.assigned_operations:
            if matches(args, op["tests"]):
                return op["function"]

        return self.default_function

    """
    Calls the first of the assigned operators (in decrescent order of
    assignment time) whose tests match `args`.
    """
    def __call__(self, *args):
        op = self.operator_for(*args)
        return op(*args)

    def __str__(self):
        return "_GenericOperator('{name}', {arity}, {default_function})".format(**vars(self))

    def __unicode__(self):
        return self.__str__

    def __repl__(self):
        return self.__str__

    """
    Assigns `function` to arguments whose elements match `tests`.

    Parameters:

    - function: the function that will perform the operation in this case
    - tests: an iterable containing functions to test the generic operator
      arguments.
    """
    def assign(self, function, tests):
        self.assigned_operations.append({
            "function": function,
            "tests": tests
        })

"""
Makes and jeturns a generic operator with a given name.

Parameters:

- arity: the number of arguments of the operator
- default_function: the function that will be called if there are no
  assigned operators.

Returns a `_GenericOperator` object to be used as a callable operator.
"""
def make_generic_operator(arity, name, default_function):
    generic_operators[name] = _GenericOperator(name, arity, default_function)
    return generic_operators[name]


"""
Assigns `function` to the generic operator `name`, when the operator's
arguments match `tests`.

A generic operator called `name` must have already been created, and its
arity must match the size of `tests`.

If several tests use the same name and function, you can call
`assign_operation` only once, with `tests` being a sequence of different
tests that will call this function.

So, instead of:

>>> assign_operation("mul", my_function, [is_foo, is_bar])
>>> assign_operation("mul", my_function, [is_bar, is_foo])

You can do:

>>> assign_operation("mul", my_function, ([is_foo, is_bar], [is_bar, is_foo]))

Parameters:

- name: the name of the generic operator
- function: the function that will perform the operation in this case
- tests: an iterable containing functions to test the generic operator
  arguments.
"""
def assign_operation(name, function, tests):
    def is_iter(thing):
        return isinstance(thing, Iterable)

    assert name in generic_operators, "Operator '{name}' does not exist".format(**vars())

    gen_op = generic_operators[name]

    assert is_iter(tests) and len(tests) > 0

    my_tests_iter = is_iter(tests[0]) and tests or [tests]

    for tests in my_tests_iter:
        assert len(tests) == gen_op.arity, \
            "Operator '{0}' expected arity {1}, received {1}".format(name, gen_op.arity, len(tests))

        gen_op.assign(function, tests)
