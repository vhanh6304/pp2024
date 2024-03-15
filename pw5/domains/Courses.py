from domains.BasicInfo import BasicInfo
from input import new_course


class Courses:
    def __init__(self):
        self.courses: list[BasicInfo] = []

    def new_course(self):
        new_course(self.courses)
