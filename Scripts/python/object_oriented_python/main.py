from course import Course
from teacher import Teacher
from student import Student

if __name__ == '__main__':
    s = Student("Keshav", 34)
    t = Teacher("Archana")
    c = Course("English", 3)
    s.set_course(c)
    t.set_course(c)
    c2 = Course("Science", 2)
    s.set_course(c2)
    print("Student Details")
    print(s.get_name())
    print(s.get_age())
    print(s.get_course())
    for course in s.get_course():
        print(course.get_name(), course.get_level())

