import os

os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ['KIVY_HOME'] = os.getcwd() + '/conf'

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import numpy as np
import re
from helper import Helper


class MainWidget(FloatLayout):
    def __init__(self):
        super().__init__()
        self.rules = {}

        self.matrix = np.array([["          ", "+", "*", "(", ")", "i", "#"],
                                ["E", "", "", "TEV", "", "TEV", ""],
                                ["EV", "+TEV", "", "", "ε", "", "ε"],
                                ["T", "", "", "FTV", "", "FTV", ""],
                                ["TV", "ε", "*FTV", "", "ε", "", "ε"],
                                ["F", "", "", "(E)", "", "i", ""]])

        grid_layout = GridLayout()
        self.add_widget(grid_layout)
        grid_layout.size_hint = (1, 0.85)
        grid_layout.pos_hint = {'top': 1}
        grid_layout.cols = len(self.matrix[0])
        grid_layout.rows = len(self.matrix)

        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[0])):
                if i == 0 and j == 0:
                    self.text_input = TextInput(text=self.matrix[i][j], id=str(i) + "," + str(j), readonly=True,
                                                font_size="0sp")
                    grid_layout.add_widget(self.text_input)
                    self.text_input.bind(text=self.on_text)
                else:
                    self.text_input = TextInput(text=self.matrix[i][j], id=str(i) + "," + str(j), multiline=False,
                                                font_size="33sp")
                    grid_layout.add_widget(self.text_input)
                    self.text_input.bind(text=self.on_text)

        box_layout = BoxLayout()
        self.add_widget(box_layout)
        box_layout.size_hint = (1, 0.15)
        self.expr = TextInput(text='(3+334)*2', font_size="40sp", halign="center", padding_y=[20, 0])
        box_layout.add_widget(self.expr)
        validate = Button(text="Validate!", id="validate", font_size="40sp")
        validate.bind(on_press=self.validate_value)
        box_layout.add_widget(validate)
        self.result = Label(text="", font_size="40sp")
        box_layout.add_widget(self.result)

    def validate_value(self, instance):
        st_aut = StackAutomaton("E", self.rules, self.expr.text)
        if st_aut.accepted:
            self.result.text = "True"
        else:
            self.result.text = "False"

    def on_text(self, instance, value):
        i = int(instance.id.split(",")[0])
        j = int(instance.id.split(",")[1])
        self.matrix[i, j] = value
        self.load_rules()

    def load_rules(self):
        for i in range(1, len(self.matrix)):  # number of rows
            for j in range(1, len(self.matrix[0])):  # number of columns
                if self.matrix[i][j] != '' and self.matrix[i][j] != "pop":
                    lista = []
                    for k in range(0, len(self.matrix[i][j])):
                        if self.matrix[i][j][k] == "ε":
                            break
                        elif k < len(self.matrix[i][j]) - 1 and self.matrix[i][j][k + 1] == "V":
                            lista.append(self.matrix[i][j][k] + "V")
                        elif self.matrix[i][j][k] != "V":
                            lista.append(self.matrix[i][j][k])
                    self.rules[Helper(self.matrix[0][j], self.matrix[i][0])] = lista


class StackAutomaton:

    def __init__(self, start_symbol, grammar, expr):
        self.automaton_stack = []
        self.expr = re.sub("[0-9]+", "i", "{0}#".format(expr))
        self.start_symbol = start_symbol
        self.grammar = grammar
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


class MainApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    MainApp().run()
