import math
import numpy as np


class Mark:
    def __init__(self, id: str, attendance: float = -1, midterm: float = -1, final: float = -1):
        self.attendance: float = attendance
        self.midterm: float = midterm
        self.final: float = final
        self.__gpa: float = -1
        self.course_id: str = id

    @property
    def gpa(self) -> float:
        """Return the GPA of the course."""
        if self.__gpa == -1:
            self.__calculate_gpa()
        return self.__gpa

    @gpa.setter
    def gpa(self, gpa: float) -> None:
        self.__gpa = gpa

    def marks(self, mark: dict[str, float]) -> None:
        self.attendance = math.floor(mark["attendance"] * 10) / 10
        self.midterm = math.floor(mark["midterm"] * 10) / 10
        self.final = math.floor(mark["final"] * 10) / 10

    def __calculate_gpa(self) -> float:
        self.attendance = 0 if self.attendance == -1 else self.attendance
        self.midterm = 0 if self.midterm == -1 else self.midterm
        self.final = 0 if self.final == -1 else self.final

        numpy_score = np.array([self.attendance, self.midterm, self.final])
        numpy_score_weight = np.array([0.1, 0.3, 0.6])

        self.__gpa = round(float(np.sum(numpy_score * numpy_score_weight)), 2)  # type: ignore
        return self.__gpa
