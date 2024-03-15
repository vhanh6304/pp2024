import os
import sys
import random
import textwrap
from datetime import datetime
from domains import *


def main():
    classroom = Classroom()
    courses = Courses()

    last_message = ""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        if last_message:
            print(last_message + "\n")
            last_message = ""

        print(f"{BCOLORS.HEADER}Student Mark Management System{BCOLORS.ENDC}")
        print("=" * 30)

        _B, _E = BCOLORS.OKBLUE, BCOLORS.ENDC
        print(
            textwrap.dedent(
                f"""\
            {_B}[1]{_E} Add student
            {_B}[2]{_E} Add course
            {_B}[3]{_E} Add mark
            {_B}[4]{_E} Show student marks
            {_B}[6]{_E} Add sample data
            {_B}[7]{_E} Sort by GPA
            {_B}[5]{_E} Exit\
            """
            )
        )

        choice = input("Choose one of the above options: ")

        while True:
            try:
                choice = int(choice)
                if choice not in range(1, 8):
                    raise ValueError
                break
            except ValueError:
                choice = input(f"{BCOLORS.FAIL}invalid choice, try again: {BCOLORS.ENDC}")

        match choice:
            case 1:
                classroom.new_student()
            case 2:
                courses.new_course()
            case 3:  # New mark
                if not classroom.students:
                    last_message = f"{BCOLORS.FAIL}No student data found, please add student data first{BCOLORS.ENDC}"
                    continue
                if not courses.courses:
                    last_message = f"{BCOLORS.FAIL}No course data found, please add course data first{BCOLORS.ENDC}"
                    continue
                classroom.new_marks(courses.courses)
            case 4:  # Show student marks
                print()
                classroom.print_table(courses.courses)
            case 5:  # Exit
                break
            case 6:  # Add sample data
                STUDENTS_DATA: list[Student] = []
                COURSES_DATA: list[BasicInfo] = []

                # Random student data
                for _ in range(5):
                    random_id = f"BI20-{random.randint(100, 999)}"
                    while random_id in [student.id for student in STUDENTS_DATA]:
                        random_id = f"BI20-{random.randint(100, 999)}"
                    random_name = random.choice(
                        ["Alice", "John", "Bob", "Mary", "Jane", "Peter", "Paul", "Mark", "Sarah", "Sara"]
                    )
                    random_dob = f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(1990, 2000)}"
                    STUDENTS_DATA.append(
                        Student(student_id=random_id, name=random_name, dob=datetime.strptime(random_dob, "%d/%m/%Y"))
                    )

                # Random courses data
                for _ in range(5):
                    random_id = f"subject-{random.randint(100, 999)}"
                    while random_id in [course.id for course in COURSES_DATA]:
                        random_id = f"subject-{random.randint(100, 999)}"

                    course_random_list = [
                        "Maths",
                        "Physics",
                        "Chemistry",
                        "Biology",
                        "English",
                        "History",
                        "Geography",
                        "Computer Science",
                        "Art",
                        "Music",
                    ]
                    random_course = random.choice(course_random_list)
                    while random_course in [course.name for course in COURSES_DATA]:
                        random_course = random.choice(course_random_list)
                        if len(COURSES_DATA) >= len(course_random_list):
                            break

                    COURSES_DATA.append(BasicInfo(id=random_id, name=random_course))

                # Random marks data for each student in each course
                for student in STUDENTS_DATA:
                    for course in COURSES_DATA:
                        attendance, midterm, final = random.randint(0, 20), random.randint(0, 20), random.randint(0, 20)
                        student.add_mark(Mark(course.id, attendance, midterm, final))
                last_message = f"{BCOLORS.OKGREEN}sample data added{BCOLORS.ENDC}"

                classroom.students = STUDENTS_DATA
                courses.courses = COURSES_DATA

            case 7:  # Sort by GPA
                classroom.sort_by_gpa()
                last_message = f"{BCOLORS.OKGREEN}descending sorted by GPA{BCOLORS.ENDC}"
            case _:
                pass
        input("\npress enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{BCOLORS.FAIL}\nexiting...{BCOLORS.ENDC}")
        sys.exit(0)
