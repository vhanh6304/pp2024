from input import new_student
from output import print_table
from domains.BasicInfo import BasicInfo
from domains.Student import Student
from input import new_marks


class Classroom:
    def __init__(self):
        self.students: list[Student] = []

    def sort_by_gpa(self) -> None:
        self.students.sort(key=lambda student: student.gpa, reverse=True)

    def new_student(self):
        new_student(self.students)

    def print_table(self, courses: list[BasicInfo]) -> None:
        print_table(self.students, courses)

    def new_marks(self, courses: list[BasicInfo]):
        new_marks(self.students, courses)
