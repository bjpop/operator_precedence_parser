'''
Module      : parse
Description : An operator precedence parser.
              Used as an example program for teaching purposes.
Copyright   : (c) Bernie Pope, 15 April 2020
License     : BSD 3-clause
Maintainer  : bjpope@unimelb.edu.au
Portability : POSIX

The accepted language of expressions consists of binary operators
written between their arguments. Arguments can be variable names
or integers. Valid operators are: * / + -

* and / take precedence over + and -

When two operators with the same precedence compete for an
argument we associate to the left (the left operator wins).

Example valid inputs:
    x
    12
    y + z
    foo * bar / zoo - 42
'''


# Valid operators and their level of precedence.
# Higher precedence numbers indicate higher precedence.
# Operators with higher precedence bind more tightly to their
# arguments than operators with lower precedence.
OPERATORS = {"*": 2, "/": 2, "+": 1, "-": 1}


def takes_precedence(op1, op2):
    ''' Test if the first operator takes precedence over the second operator.

    Arguments:
        op1: operator name, a string
        op2: operator name, a string
    Result:
        A boolean. True if op1 takes precedence over op2.
    Assumptions:
        op1 and op2 must be valid operator names. See: valid_op
        to test for valid operator names.
    '''
    return OPERATORS[op1] >= OPERATORS[op2]


def valid_op(token):
    ''' Test if a token is a valid operator name.

    Arguments:
        token: a token from the input language of operator expressions, a string.
    Result:
        A boolean. True if token is a valid operator name.
    '''
    return token in OPERATORS


def valid_arg(token):
    ''' Test if a token is a valid argument. Arguments can be either
    integers or variable names. Variable names consist only of alphabetic
    characters, and must be non-empty.

    Arguments:
        token: a token from the input language of operator expressions, a string.
    Result:
        A boolean. True if token is a valid argument.
    '''
    return len(token) > 0 and (token.isdigit() or token.isalpha())


def lex(string):
    '''Split an input string into a list of tokens. Tokens
    are separated by whitespace. Note that this function does
    not check that the resulting tokens are valid.

    Arguments:
        string: an input string containing an expression
    Result:
        A boolean. True if token is a valid argument.
    '''
    return string.split()


class Parser:
    '''A shift-reduce parser for the operator precedence
    language.

    Note: to use the parser you must call the parse method.
    '''


    def __init__(self):
        '''Initialise a new Parser.

        Note: to use the parser you must call the parse method.
        '''
        # We set all the attributes to None. They are properly
        # initialised in the parse method.
        self.ops = None
        self.args = None
        self.state = None
        self.index = None
        self.toks = None


    def parse(self, string):
        '''Parse an input expression and, if successful return
        an expression tree representing the correct association
        of operators to their arguments.

        Arguments:
            string: an input string containing an expression
        Result:
            An expression tree on success, or None on failure.

            Operator applications are represented as 3-tuples.
            Variables and integers are represented as strings.

            For example:
            >>> p.parse("3 * 2 + 6 / 4")
            (("3", "*", "2"), "+", ("6", "/", "4"))
        Side effects:
            This method modifies the internal state of the Parser
            object. At the end of calling this method the state
            will represent the final configuration of the
            shift-reduce parsing machine. Calling this method
            re-initialises the state.
        '''
        # Operator stack
        self.ops = []
        # Argument stack
        self.args = []
        # State of the parser, can be "arg", "op" or "end"
        #    arg state parses argument tokens
        #    op state parsers operator tokens
        #    end state terminates the parse (maybe error or success)
        self.state = "arg"
        # list of tokens from the input expression
        self.toks = lex(string)
        # Index into the list of tokens
        self.index = 0

        # Iterate the parsing machine until we reach the end state
        while self.state != "end":
            if self.state == "arg":
                # If we are in the arg state then shift the next token
                # onto the arg stack
                self.shift_arg()
            elif self.state == "op":
                if self.terminated():
                    # If we have reached a terminating state then
                    # end the parse
                    self.state = "end"
                elif self.reducible():
                    # If the operator on top of the op-stack is
                    # reducible then perform a reduction, stay in the
                    # op state
                    self.reduce()
                else:
                    # Shift the next token onto the operator stack
                    # and go to the arg state
                    self.shift_op()

        if self.terminated() and len(self.args) == 1:
            # We have terminated the parse successfully.
            # Return the top (and only value) from the arg stack
            # as the result.
            return self.args[0]

        # The parse failed.
        return None


    def next_tok(self):
        '''If possible, get the next token from the input, but do not
        advance the token index.

        Arguments:
            self: the parser object
        Result:
            The next token from the input (a string), or None
            if there are no tokens left to process.
        '''
        if self.index < len(self.toks):
            return self.toks[self.index]
        return None


    def peek_ops(self):
        '''If possible, get the operator from the top of the op-stack,
        but do not remove it. See: pop_ops for a method which does remove
        the item from the stack.

        Arguments:
            self: the parser object
        Result:
            The operator from the top of the op-stack (a string), or None
            if the op-stack is empty.
        '''
        if self.ops:
            return self.ops[-1]
        return None


    def pop_ops(self):
        '''If possible, pop the operator from the top of the op-stack
        and return its value. See: peek_ops for a method which does
        not remove the item from the stack.

        Arguments:
            self: the parser object
        Result:
            The argument from the top of the op-stack (a string), or None
            if the op-stack is empty.
        Side effects:
            This method may modify the op-stack by removing the top item.
        '''
        if self.ops:
            return self.ops.pop()
        return None


    def pop_args(self):
        '''If possible, pop the argument from the top of the arg-stack
        and return its value.

        Arguments:
            self: the parser object
        Result:
            The argument from the top of the arg-stack (a string), or None
            if the arg-stack is empty.
        Side effects:
            This method may modify the arg-stack by removing the top item.
        '''
        if self.args:
            return self.args.pop()
        return None


    def terminated(self):
        '''Test if the parser has reached a terminating configuration.
        This occurs when both of the following conditions hold:
            - the operator stack is empty
            - there are no more tokens in the input

        Arguments:
            self: the parser object
        Result:
            boolean, True if the parser has reached a terminating configuration
            and False otherwse.
        '''
        return not (self.ops or self.next_tok())


    def shift_op(self):
        '''If possible, shift the next operator token from the inputs
        onto the top of the op-stack, and transition to the
        arg state.

        If the input tokens are exhausted, or the next token is not
        a valid operator then transition to the end state because
        the parse failed.

        Arguments:
            self: the parser object
        Result:
            None
        Side effects:
            If successful, move to the next token in the input
            by incrementing the index attribute, and
            transition to the arg state. Push the next token
            onto the op-stack.
            If unsuccessful, transition to the end state.
        '''
        tok = self.next_tok()
        if tok and valid_op(tok):
            # push the next token onto the op-stack
            self.ops.append(tok)
            self.index += 1
            self.state = "arg"
        else:
            self.state = "end"


    def shift_arg(self):
        '''If possible, shift the next operator token from the inputs
        onto the top of the arg-stack, and transition to the
        op state.

        If the input tokens are exhausted, or the next token is not
        a valid argument then transition to the end state because
        the parse failed.

        Arguments:
            self: the parser object
        Result:
            None
        Side effects:
            If successful, move to the next token in the input
            by incrementing the index attribute, and
            transition to the op state. Push the next token
            onto the arg-stack.
            If unsuccessful, transition to the end state.
        '''
        tok = self.next_tok()
        if tok and valid_arg(tok):
            # push the next token onto the op-stack
            self.args.append(tok)
            self.index += 1
            self.state = "op"
        else:
            self.state = "end"


    def reducible(self):
        '''Test if the shift-reduce parse machine is in
        a reducible state.

        This is true when:
            - there is an operator on top of the op-stack:
              AND
                  - there are no more tokens in the input
                    OR
                  - the operator on top of the op-stack
                    takes precedence over the next input
                    token

        Arguments:
            self: the parser object
        Result:
            Boolean, True if the parser is in a reducible state
            and False otherwise.
        '''
        top_op = self.peek_ops()
        if top_op:
            tok = self.next_tok()
            if not tok:
                return True
            return takes_precedence(top_op, tok)
        return False


    def reduce(self):
        '''Perform a reduction by popping the top of
        the op-stack and the 2 top items on the args-stack,
        building an operator application expression tree,
        and pushing that back onto the arg-stack.

        If there are insufficient items on either the
        op-stack or the arg-stack then transition to
        the end state because a parse error has occurred.

        Arguments:
            self: the parser object
        Result:
            None
        Side effects:
            Pop the the op-stack (once) and the arg-stack (twice).
            Transition to the end state on an error.
        '''
        operator = self.pop_ops()
        arg1 = self.pop_args()
        arg2 = self.pop_args()
        if operator and arg1 and arg2:
            # Build a new expression tree for this operator application
            # to its two arguments, and push it onto the arg-stack.
            self.args.append((arg2, operator, arg1))
        else:
            self.state = "end"


def parse_test(string, expected):
    '''A test harness for the parser. Try to parse an
    input string representing an expression and check whether the
    result is the same as the expected value. Print a detailed
    error message on failure.

    Arguments:
        string: a possibly empty input string to be parsed
        expected: the expected output from the parser, an expression tree.
                  Operator applications are represented as 3-tuples, and
                  integers and variables are represented as strings.
    Result:
        None
    Side effects:
        Print "PASS" on success, or a detailed error message on failue.
    '''
    this_parser = Parser()
    tree = this_parser.parse(string)
    correct = tree == expected
    if correct:
        print("PASS")
    else:
        print(f"FAIL input: {string}, expected: {expected}, output: {tree}, correct: {correct}")


# Test inputs
TEST1 = ""
TEST2 = "*"
TEST3 = "?"
TEST4 = "3"
TEST5 = "3 + 2"
TEST6 = "3 + 2 * 6"
TEST7 = "3 * 2 + 6"
TEST8 = "3 * 2 + 6 / 4"
TEST9 = "3 +"
TEST10 = "3 4"


# Test the parser on test inputs and see if the result is correct
parse_test(TEST1, None)
parse_test(TEST2, None)
parse_test(TEST3, None)
parse_test(TEST4, "3")
parse_test(TEST5, ("3", "+", "2"))
parse_test(TEST6, ("3", "+", ("2", "*", "6")))
parse_test(TEST7, (("3", "*", "2"), "+", "6"))
parse_test(TEST8, (("3", "*", "2"), "+", ("6", "/", "4")))
parse_test(TEST9, None)
parse_test(TEST10, None)
