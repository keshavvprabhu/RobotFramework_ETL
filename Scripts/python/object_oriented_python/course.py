class Course:
    def __init__(self, name:str, level:int):
        self.name = name
        self.level = level

    def get_name(self):
        return self.name

    def get_level(self):
        return self.level

    def set_name(self, name):
        self.name = name

    def set_level(self, level):
        self.level = level


if __name__ == '__main__':
    pass