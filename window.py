import os
os.environ['KIVY_HOME'] = os.getcwd() + '/conf'
os.environ["KIVY_NO_CONSOLELOG"] = "1"
from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
import numpy as np
from helper import Helper
from stack_automaton import StackAutomaton
Config.set("graphics", "resizable", '0')


class MainWidget(FloatLayout):
    def __init__(self):
        super().__init__()
        self.matrix = np.array([["          ", "+", "*", "(", ")", "i", "#"],
                                ["E", "", "", "TEV", "", "TEV", ""],
                                ["EV", "+TEV", "", "", "ε", "", "ε"],
                                ["T", "", "", "FTV", "", "FTV", ""],
                                ["TV", "ε", "*FTV", "", "ε", "", "ε"],
                                ["F", "", "", "(E)", "", "i", ""]])
        self.number_of_columns = len(self.matrix[0])
        self.number_of_rows = len(self.matrix)
        self.rules = {}
        self.expr = TextInput(text='(3+334)*2', font_size="40sp", halign="center", padding_y=[20, 0])
        self.result = Label(text="", font_size="40sp")
        self.recycle_view = RecycleView()
        self.create_layouts()

    def create_layouts(self):
        self.create_grid_layout()
        self.create_box_layout()
        self.create_recycle_view()

    def create_grid_layout(self):
        grid_layout = GridLayout()
        grid_layout.size_hint = (1, 0.6)
        grid_layout.pos_hint = {'top': 1}
        grid_layout.cols = self.number_of_columns
        grid_layout.rows = self.number_of_rows
        self.add_text_inputs_to_grid_layout(grid_layout)
        self.add_widget(grid_layout)

    def add_text_inputs_to_grid_layout(self, grid_layout):
        for row_index in range(0, self.number_of_rows):
            for column_index in range(0, self.number_of_columns):
                if row_index == 0 and column_index == 0:
                    text_input = TextInput(text=self.matrix[row_index][column_index],
                                           id=str(row_index) + "," + str(column_index),
                                           readonly=True,
                                           font_size="0sp")
                    grid_layout.add_widget(text_input)
                    text_input.bind(text=self.on_text)
                else:
                    text_input = TextInput(text=self.matrix[row_index][column_index],
                                           id=str(row_index) + "," + str(column_index),
                                           multiline=False,
                                           font_size="33sp")
                    grid_layout.add_widget(text_input)
                    text_input.bind(text=self.on_text)

    def on_text(self, instance, value):
        row_index = int(instance.id.split(",")[0])
        column_index = int(instance.id.split(",")[1])
        self.matrix[row_index, column_index] = value
        self.load_rules()

    def load_rules(self):
        comma = 'V'
        epsilon = 'ε'
        pop = "pop"
        for row_index in range(1, self.number_of_rows):
            for column_index in range(1, self.number_of_columns):
                len_of_matrix_current_element = len(self.matrix[row_index][column_index])
                if self.matrix[row_index][column_index] != '' and self.matrix[row_index][column_index] != pop:
                    list_of_rules = []
                    for element_of_matrix in range(0, len_of_matrix_current_element):
                        if self.matrix[row_index][column_index][element_of_matrix] == epsilon:
                            break
                        elif element_of_matrix < len_of_matrix_current_element - 1 and \
                                self.matrix[row_index][column_index][element_of_matrix + 1] == comma:
                            list_of_rules.append(self.matrix[row_index][column_index][element_of_matrix] + comma)
                        elif self.matrix[row_index][column_index][element_of_matrix] != comma:
                            list_of_rules.append(self.matrix[row_index][column_index][element_of_matrix])
                    self.rules[Helper(self.matrix[0][column_index], self.matrix[row_index][0])] = list_of_rules

    def create_box_layout(self):
        box_layout = BoxLayout()
        box_layout.size_hint = (1, 0.15)
        box_layout.pos_hint = {'top': 0.4}
        box_layout.add_widget(self.expr)
        self.create_validation_button(box_layout)
        box_layout.add_widget(self.result)
        self.add_widget(box_layout)

    def create_validation_button(self, box_layout):
        validate = Button(text="Validate!", id="validate", font_size="40sp")
        validate.bind(on_press=self.validate_value)
        box_layout.add_widget(validate)

    def validate_value(self, instance):
        st_aut = StackAutomaton("E", self.rules, self.expr.text)
        if st_aut.accepted:
            self.result.text = "True"
        else:
            self.result.text = "False"
        self.refresh_view(st_aut.steps)

    def create_recycle_view(self):
        recycle_box_layout = RecycleBoxLayout()
        recycle_box_layout.default_size = (None, dp(40))
        recycle_box_layout.default_size_hint = (1, None)
        recycle_box_layout.size_hint_y = None
        recycle_box_layout.orientation = 'vertical'
        recycle_box_layout.bind(minimum_height=recycle_box_layout.setter("height"))
        self.recycle_view.size_hint = (1, 0.24)
        self.recycle_view.pos_hint = {'top': 0.24}
        self.recycle_view.add_widget(recycle_box_layout)
        self.recycle_view.viewclass = 'Label'
        self.add_widget(self.recycle_view)
        self.recycle_view.data = []

    def refresh_view(self, data_list):
        self.recycle_view.data = data_list


class MainApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    MainApp().run()
