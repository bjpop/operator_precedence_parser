operators = {"*": 2, "/": 2, "+": 1, "-": 1}

def takes_precedence(op1, op2):
    return operators[op1] > operators[op2]

def valid_op(tok):
    return tok in operators

def valid_arg(tok):
    return tok.isdigit() or tok.isalpha()

def lex(str):
    return str.split()

class Parser:

    def parse(self, string):
        self.ops = []
        self.args = []
        self.state = "arg"
        self.index = 0
        self.toks = lex(string)

        while self.state != "end":
            if self.state == "arg":
                self.shift_arg()
            elif self.state == "op":
                if self.terminated():
                    self.state = "end"
                elif self.reducible():
                    self.reduce()
                else:
                    self.shift_op()

        if self.terminated() and len(self.args) == 1:
            return self.args[0]
        else:
            return None

    def next_tok(self):
        if self.index < len(self.toks):
            return self.toks[self.index]
        else:
            return None

    def peek_ops(self):
        if self.ops:
            return self.ops[-1]
        else:
            return None

    def pop_args(self):
        if self.args:
            return self.args.pop()
        else:
            return None

    def pop_ops(self):
        if self.ops:
            return self.ops.pop()
        else:
            return None

    def terminated(self):
        return not (self.ops or self.next_tok())

    def shift_op(self):
        tok = self.next_tok()
        if tok and valid_op(tok):
            self.ops.append(tok)
            self.index += 1
            self.state = "arg"
        else:
            self.state = "end" 

    def shift_arg(self):
        tok = self.next_tok()
        if tok and valid_arg(tok):
            self.args.append(tok)
            self.index += 1
            self.state = "op"
        else:
            self.state = "end"

    def reducible(self):
        top_op = self.peek_ops()
        if top_op: 
            tok = self.next_tok()
            if not tok:
                return True
            else:
                return takes_precedence(top_op, tok)
        else:
            return False

    def reduce(self):
        op = self.pop_ops()
        arg1 = self.pop_args()
        arg2 = self.pop_args()
        if op and arg1 and arg2:
            self.args.append((arg2, op, arg1))
        else:
            self.state = "end" 


def parse_test(string, expected):
    p = Parser()
    tree = p.parse(string)
    correct = tree == expected
    if correct:
        print("PASS")
    else:
        print(f"FAIL input: {string}, expected: {expected}, output: {tree}, correct: {correct}")

test1 = ""
test2 = "*"
test3 = "?"
test4 = "3"
test5 = "3 + 2"
test6 = "3 + 2 * 6"
test7 = "3 * 2 + 6"
test8 = "3 * 2 + 6 / 4"
test9 = "3 +"

parse_test(test1, None)
parse_test(test2, None)
parse_test(test3, None)
parse_test(test4, "3")
parse_test(test5, ("3", "+", "2"))
parse_test(test6, ("3", "+", ("2", "*", "6")))
parse_test(test7, (("3", "*", "2"), "+", "6"))
parse_test(test8, (("3", "*", "2"), "+", ("6", "/", "4")))
parse_test(test9, None)

