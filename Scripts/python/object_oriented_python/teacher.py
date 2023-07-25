from course import Course

class Teacher:
    def __init__(self, name):
        self.name = name
        self.course = list()

    def set_course(self, course):
        self.course.append(course)

    def get_courses(self):
        return self.course


if __name__ == '__main__':
    pass