class Helper:
    def __init__(self, character, current):
        self.character = character
        self.current = current

    def __eq__(self, other):
        if other is None or type(self) != type(other):
            return False
        if self.character == other.character and self.current == other.current:
            return True
        return False

    def __hash__(self):
        return hash((self.character, self.current))
