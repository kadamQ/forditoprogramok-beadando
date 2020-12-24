import re
from helper import Helper


class StackAutomaton:

    def __init__(self, start_symbol, grammar, expr):
        self.automaton_stack = []
        self.expr = re.sub("[0-9]+", "i", "{0}#".format(expr))
        self.start_symbol = start_symbol
        self.grammar = grammar
        self.steps = []
        self.step = 1
        self.accepted = False
        self.solve()

    def solve(self):
        self.automaton_stack.append("#")
        self.automaton_stack.append(self.start_symbol)
        index = 0
        while len(self.automaton_stack) != 0:
            c = self.expr[index]
            top = self.automaton_stack.pop()
            helper = Helper(c, top)
            self.steps.append({'text': str(self.step) + ". step: " + self.expr[index:] + ', Current elements in the stack: ' + str(self.automaton_stack)})
            self.step += 1
            if c == top:
                index += 1
                continue
            if helper in self.grammar:
                next_step = self.grammar.get(helper)
                reverse = []
                for i in range(len(next_step) - 1, -1, -1):
                    reverse.append(next_step[i])
                for s in reverse:
                    self.automaton_stack.append(s)
            else:
                break
        if len(self.automaton_stack) == 0 and self.expr[index - 1] == "#":
            self.accepted = True
