import os
import re
import sys
import random
from textwrap import dedent

STUDENTS: list[dict[str, str | list[dict[str, str | float]]]] = []
"""
[
    {
        "name": "Nguyen Van A",
        "id": "1",
        "dob": "2000-01-01",
        "marks": [
            {
                "course_id": "1",
                "mark": 10.0
            },
    }
]
"""

COURSES: list[dict[str, str]] = []
"""
[
    {
        "name": "Math",
        "id": "1"
    },
]
"""


class BCOLORS:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def get_user_selection(options: list[str], default: int = 0) -> int:
    """Get user selection from a list of options and return the index of the selected option"""
    for i, option in enumerate(options):
        print(f"{BCOLORS.OKGREEN}{i+1}. {option}{BCOLORS.ENDC}")
    choice = input(f"choose one of the above options (default: {default+1}): ")
    while True:
        try:
            if choice == "":
                return default
            choice = int(choice)
            if choice not in range(1, len(options) + 1):
                raise ValueError
            return choice - 1
        except ValueError:
            choice = input(f"{BCOLORS.FAIL}invalid choice, try again: {BCOLORS.ENDC}")


def get_user_input_number(prompt: str, default: int = 0) -> int:
    choice = input(f"{prompt} (default: {default}): ")
    while True:
        try:
            if choice == "":
                return default
            choice = int(choice)
            return choice
        except ValueError:
            choice = input(f"{BCOLORS.FAIL}invalid choice, try again: {BCOLORS.ENDC}")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def add_student() -> None:
    student_name = input("\nenter student name: ")

    student_id = input("enter student id: ")
    while True:
        if not re.match(r"BI\d{2}-\d{3}", student_id):
            student_id = input(f"{BCOLORS.FAIL}invalid id, try again: {BCOLORS.ENDC}")
            continue
        if next((True for student in STUDENTS if student["id"] == student_id), False):
            student_id = input(f"{BCOLORS.FAIL}id already exists, try again: {BCOLORS.ENDC}")
            continue
        break

    student_dob = input("enter student date of birth: ")
    while True:
        if not re.match(r"\d{4}-\d{2}-\d{2}", student_dob):
            student_dob = input(f"{BCOLORS.FAIL}invalid date of birth, try again: {BCOLORS.ENDC}")
            continue
        break

    marks: list[dict[str, str | float]] = []
    STUDENTS.append({"name": student_name, "id": student_id, "dob": student_dob, "marks": marks})


def add_course() -> None:
    course_name = input("enter course name: ")
    while True:
        for course in COURSES:
            if course["name"] == course_name:
                course_name = input(f"{BCOLORS.FAIL}course already exists, try again: {BCOLORS.ENDC}")
                break
        else:
            break

    course_id = input("enter course id: ")
    while True:
        for course in COURSES:
            if course["id"] == course_id:
                course_id = input(f"{BCOLORS.FAIL}id already exists, try again: {BCOLORS.ENDC}")
                break
        else:
            break

    COURSES.append({"name": course_name, "id": course_id})


def add_mark() -> None:
    student_id = get_user_selection([student["id"] for student in STUDENTS], 0)
    course_id = get_user_selection([course["name"] for course in COURSES], 0)

    _mark = input("enter mark: ")
    while True:
        try:
            mark = float(_mark)
            if mark < 0 or mark > 20:
                raise ValueError
            break
        except ValueError:
            _mark = input(f"{BCOLORS.FAIL}invalid mark, try again: {BCOLORS.ENDC}")

    for student in STUDENTS:
        if student["id"] == STUDENTS[student_id]["id"]:
            marks: list[dict[str, str | float]] = student["marks"]
            marks.append({"course_id": course_id, "mark": mark})
            break


def format_str(content: str, width: int) -> str:
    return f"| {content}{' '*(width-len(content))} "


def print_table() -> None:
    data_column_content = ["Data", "ID", "DOB"]
    data_column_content.extend([f"Course: {course['name']}" for course in COURSES])
    data_column_width = max([len(content) for content in data_column_content])
    del data_column_content

    width_for_each_student_column: list[int] = []
    for student in STUDENTS:
        student_column_content = [student["name"], student["id"], student["dob"]]
        for mark in student["marks"]:
            student_column_content.append(str(mark["mark"]))
        width_for_each_student_column.append(max([len(content) for content in student_column_content]))

    # First row
    print(format_str("Data", data_column_width), end="")
    for i, student in enumerate(STUDENTS):
        print(format_str(student["name"], width_for_each_student_column[i]), end="")
    print()

    # Seperator row
    print("=" * (data_column_width + 3), end="")
    for width in width_for_each_student_column:
        print("=" * (width + 3), end="")
    print()

    print(format_str("ID", data_column_width), end="")
    for i, student in enumerate(STUDENTS):
        print(format_str(student["id"], width_for_each_student_column[i]), end="")
    print()

    print(format_str("DOB", data_column_width), end="")
    for i, student in enumerate(STUDENTS):
        print(format_str(student["dob"], width_for_each_student_column[i]), end="")
    print()

    for course in COURSES:
        print(format_str(f"Course: {course['name']}", data_column_width), end="")
        for i, student in enumerate(STUDENTS):
            for mark in student["marks"]:
                if mark["course_id"] == course["id"]:
                    print(format_str(str(mark["mark"]), width_for_each_student_column[i]), end="")
                    break
            else:
                print(format_str("", width_for_each_student_column[i]), end="")
        print()


def main():
    last_message = ""
    while True:
        clear_screen()
        print(last_message + "\n") if last_message else None
        last_message = ""

        _B = BCOLORS.OKBLUE
        _E = BCOLORS.ENDC
        print(f"{BCOLORS.HEADER}Student Mark Management System{_E}")
        print(
            dedent(
                f"""\
            {_B}[1]{_E} Add student
            {_B}[2]{_E} Add course
            {_B}[3]{_E} Add mark
            {_B}[4]{_E} Show student marks
            {_B}[5]{_E} Exit
            {'-' * 20}
            {_B}[6]{_E} Add sample data
        """
            )
        )
        _choice = input("Choose one of the above options: ")
        while True:
            try:
                choice = int(_choice)
                if choice not in range(1, 7):
                    raise ValueError
                break
            except ValueError:
                _choice = input(f"{BCOLORS.FAIL}invalid choice, try again: {BCOLORS.ENDC}")

        match choice:
            case 1:
                number_of_students_to_add = get_user_input_number("how many students do you want to add", 1)
                for _ in range(number_of_students_to_add):
                    add_student(STUDENTS)
            case 2:
                number_of_courses_to_add = get_user_input_number("how many courses do you want to add", 1)
                for _ in range(number_of_courses_to_add):
                    add_course(COURSES)
            case 3:
                number_of_marks_to_add = get_user_input_number("how many marks do you want to add", 1)
                for _ in range(number_of_marks_to_add):
                    add_mark(STUDENTS, COURSES)
            case 4:
                print()
                print_table(STUDENTS, COURSES)
                input("\npress enter to continue...")
            case 5:
                break
            case 6:
                for _ in range(5):
                    id = f"BI20-{random.randint(100, 999)}"
                    while id in [student["id"] for student in STUDENTS]:
                        id = f"BI20-{random.randint(100, 999)}"
                    name = random.choice(["John", "Jane", "Jack", "Jill", "Jenny", "Jen", "Jenifer", "Jeniffer"])
                    dob = f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(1990, 2000)}"
                    STUDENTS.append({"id": id, "name": name, "dob": dob, "marks": []})

                for _ in range(5):
                    id = f"subject-{random.randint(100, 999)}"
                    while id in [course["id"] for course in COURSES]:
                        id = f"subject-{random.randint(100, 999)}"

                    courses_list = ["Maths", "Physics", "Chemistry", "Biology", "English", "History", "Geography"]
                    course = random.choice(courses_list)
                    while course in [course["name"] for course in COURSES]:
                        course = random.choice(courses_list)
                        if len(COURSES) >= len(courses_list):
                            break

                    COURSES.append({"id": id, "name": course})

                for student in STUDENTS:
                    for course in COURSES:
                        student_marks: list[dict[str, str | float]] = student["marks"]
                        student_marks.append({"course_id": course["id"], "mark": random.randint(0, 20)})
                last_message = f"{BCOLORS.OKGREEN}sample data added{BCOLORS.ENDC}"
            case _:
                raise ValueError


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{BCOLORS.FAIL}exiting...{BCOLORS.ENDC}")
        sys.exit(0)