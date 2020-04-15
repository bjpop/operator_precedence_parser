'''
Module      : parse_test
Description : Unit tests for the Parser class in the parse module 
Copyright   : (c) Bernie Pope, 15 April 2020
License     : BSD 3-clause
Maintainer  : bjpope@unimelb.edu.au
Portability : POSIX
'''

import unittest
from parse import Parser


class TestParser(unittest.TestCase):

    def do_test(self, input_str, expected):
        "Wrapper function for testing Parser"
        # Parse the input string
        result = Parser().parse(input_str)  
        # Check that it is equal to the expected output
        self.assertEqual(expected, result)

    def test_empty_input(self):
        self.do_test("", None)

    def test_single_operator(self):
        self.do_test("*", None)

    def test_not_operator_or_arg(self):
        self.do_test("?", None)

    def test_single_integer_arg(self):
        self.do_test("3", "3")

    def test_addition_two_args(self):
        self.do_test("3 + 2", ("3", "+", "2"))

    def test_plus_times(self):
        self.do_test("3 + 2 * 6", ("3", "+", ("2", "*", "6")))

    def test_times_plus(self):
        self.do_test("3 * 2 + 6", (("3", "*", "2"), "+", "6"))
        
    def test_times_plus_divide(self):
        self.do_test("3 * 2 + 6 / 4", (("3", "*", "2"), "+", ("6", "/", "4"))) 

    def test_plus_one_left_arg(self):
        self.do_test("3 +", None)

    def test_plus_one_right_arg(self):
        self.do_test("+ 3", None)

    def test_two_args_no_op(self):
        self.do_test("3 4", None)


if __name__ == '__main__':
    unittest.main()
