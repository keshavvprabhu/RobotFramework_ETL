from course import Course

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.course = list()

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_course(self):
        return self.course

    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

    def set_course(self, course):
        self.course.append(course)


if __name__ == '__main__':
    pass