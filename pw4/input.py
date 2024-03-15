from __future__ import annotations
import re
from datetime import datetime
from domains import *


def new_student(students: list[Student]) -> None:
    student_name = input("\nenter student name: ")
    student_id = input("enter student id (BIxx-xxx): ").upper()

    # === Verify student ID ===
    while True:
        if re.match(r"BI\d{2}-\d{3}", student_id):
            for student in students:
                if student.id == student_id:
                    student_id = input(f"{BCOLORS.FAIL}another student has the same id, try again: {BCOLORS.ENDC}").upper()
                    break
            else:
                break
        else:
            student_id = input(f"{BCOLORS.FAIL}invalid id, try again: {BCOLORS.ENDC}")

    student_dob = input("enter student date of birth (dd-mm-yyyy): ")
    while True:
        try:
            student_dob = datetime.strptime(student_dob, "%d-%m-%Y")
            break
        except:
            student_dob = input(f"{BCOLORS.FAIL}invalid date of birth, try again: {BCOLORS.ENDC}")
    students.append(Student(student_name, student_id, student_dob))


def new_marks(students: list[Student], courses: list[BasicInfo]) -> None:
    print(f"\n{BCOLORS.BOLD}Select student:{BCOLORS.ENDC}")
    student_index_selected = get_user_selection([f"{student.name} (ID {student.id})" for student in students], 0)
    student_id_selected = students[student_index_selected].id

    print(f"\n{BCOLORS.BOLD}Select course:{BCOLORS.ENDC}")
    course_index_selected = get_user_selection([f"{course.name} (ID {course.id})" for course in courses], 0)
    course_id_selected = courses[course_index_selected].id

    # === Print student's marks of the selected course if exist ===
    for _, student in enumerate(students):
        if student.id != student_id_selected:
            continue
        if len(student.courses_marks) == 0:
            break
        for course_marks in student.courses_marks:
            if course_marks.course_id != course_id_selected:
                break
            else:
                marks = course_marks.marks
                attendance, midterm, final = marks[0], marks[1], marks[2]
                print(f"{BCOLORS.BOLD}{student.name}'s mark of {courses[course_index_selected].name}: {BCOLORS.ENDC}")
                print(f"{BCOLORS.BOLD}attendance: {attendance}, midterm: {midterm}, final: {final}{BCOLORS.ENDC}")

    marks_input = input(
        "\nenter attendance, mid-term, final mark (separated by comma, _ for empty mark, mark must be in range [0, 20]): "
    ).split(",")
    marks: list[float] = [0, 0, 0]
    while True:
        try:
            if len(marks_input) != 3:
                raise ValueError
            for index, mark in enumerate(marks_input):
                if mark == "_":
                    marks[index] = -1
                mark = float(mark)
                if mark < 0 or mark > 20:
                    raise ValueError
                marks[index] = mark
            break
        except ValueError:
            marks_input = input(f"{BCOLORS.FAIL}invalid marks, try again: {BCOLORS.ENDC}").split(",")
    attendance, midterm, final = marks
    student = students[student_index_selected]

    for index, course_marks in enumerate(student.courses_marks):
        if course_marks.course_id == course_id_selected:
            student.courses_marks[index] = Mark(course_id_selected, attendance, midterm, final)
            break
    else:
        student.courses_marks.append(Mark(course_id_selected, attendance, midterm, final))


def new_course(courses: list[BasicInfo]) -> None:
    course_name_entered = input("\nenter course name: ")
    course_id_entered = input("enter course id: ")

    for course in courses:
        if course.name == course_name_entered or course.id == course_id_entered:
            print(f"{BCOLORS.FAIL}course already exists{BCOLORS.ENDC}")
            # return None
    else:
        # return BasicInfo(course_name_entered, course_id_entered)
        courses.append(BasicInfo(course_name_entered, course_id_entered))


def get_user_selection(options: list[str], default: int = 0) -> int:
    """Get user selection from a list of options and return the index of the selected option."""
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
    """Get a positive integer from user."""
    choice = input(f"{prompt} (default: {default}): ")
    while True:
        try:
            if choice == "":
                return default
            choice = int(choice)
            return choice
        except ValueError:
            choice = input(f"{BCOLORS.FAIL}invalid choice, try again: {BCOLORS.ENDC}")
