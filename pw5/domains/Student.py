from __future__ import annotations
from domains.BasicInfo import BasicInfo
from datetime import datetime
import sys

if sys.version_info >= (3, 11):
    from typing import TYPE_CHECKING
else:
    from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    from domains.Mark import Mark


class Student(BasicInfo):
    def __init__(self, name: str, student_id: str, dob: datetime):
        super().__init__(name=name, id=student_id)
        self.__dob: datetime = dob
        self.courses_marks: list[Mark] = []
        self.__gpa = -1

    @property
    def dob(self) -> str:
        return self.__dob.strftime("%Y-%m-%d")

    @property
    def gpa(self) -> float:
        return self.__gpa if self.__gpa != -1 else self.__calculate_gpa()

    @gpa.setter
    def gpa(self, gpa: float) -> None:
        self.__gpa = gpa

    def __calculate_gpa(self) -> float:
        if len(self.courses_marks) == 0:
            return 0
        total_gpa = 0
        for course_marks in self.courses_marks:
            total_gpa += course_marks.gpa
        return round(total_gpa / len(self.courses_marks), 2)

    def add_mark(self, mark: Mark) -> None:
        self.courses_marks.append(mark)
