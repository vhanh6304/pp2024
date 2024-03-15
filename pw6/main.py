import os
import sys
import random
import pickle
import textwrap
from datetime import datetime
from domains import *
from concurrent.futures import ThreadPoolExecutor

if sys.version_info >= (3, 6):
    import zipfile
else:
    import zipfile36 as zipfile


def save_to_txt(classroom: Classroom, courses: Courses):
    # get all the marks of the students into a seperate list
    # [
    #     [student_id, course_id, attendance, midterm, final]
    # ]
    marks: list[list[str | float]] = []
    for student in classroom.students:
        for mark in student.courses_marks:
            marks.append([student.id, mark.course_id, mark.attendance, mark.midterm, mark.final])

    files = ["students.txt", "courses.txt", "marks.txt"]
    for file_name in files:
        if os.path.exists(file_name):
            os.remove(file_name)

    def dump(data: list[object], file: str):
        with open(file, "wb") as f:
            pickle.dump(data, f)

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(dump, [classroom.students, courses.courses, marks], files)


def read_from_txt(classroom: Classroom, courses: Courses):
    def load_students():
        nonlocal classroom
        with open("students.txt", "rb") as f:
            classroom.students = pickle.load(f)

    def load_courses():
        nonlocal courses
        with open("courses.txt", "rb") as f:
            courses.courses = pickle.load(f)

    def load_marks():
        nonlocal classroom
        with open("marks.txt", "rb") as f:
            marks = pickle.load(f)
            for mark in marks:
                for student in classroom.students:
                    if student.id == mark[0]:
                        for course_marks in student.courses_marks:
                            if course_marks.course_id == mark[1]:
                                course_marks.attendance = float(mark[2])
                                course_marks.midterm = float(mark[3])
                                course_marks.final = float(mark[4])
                                break
                        else:
                            course_marks = Mark(mark[1], float(mark[2]), float(mark[3]), float(mark[4]))
                            student.courses_marks.append(course_marks)
                        break

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(load_students, [], [])
        executor.map(load_courses, [], [])
        executor.map(load_marks, [], [])


def main():
    classroom = Classroom()
    courses = Courses()

    if os.path.exists("students.dat"):
        for file_name in ["students.txt", "courses.txt", "marks.txt"]:
            if os.path.exists(file_name):
                os.remove(file_name)
        with zipfile.ZipFile("students.dat", "r") as zip_ref:
            zip_ref.extractall()
        read_from_txt(classroom, courses)

    last_message = ""
    while True:
        save_to_txt(classroom, courses)
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
                compression_method_select = input(
                    f"{BCOLORS.OKBLUE}Select compression method (store, fast, balanced, best): {BCOLORS.ENDC}"
                )
                while compression_method_select not in ["store", "fast", "balanced", "best"]:
                    compression_method_select = input(f"{BCOLORS.FAIL}Invalid compression method, try again: {BCOLORS.ENDC}")

                compression_method = {
                    "store": zipfile.ZIP_STORED,
                    "fast": zipfile.ZIP_DEFLATED,
                    "balanced": zipfile.ZIP_BZIP2,
                    "best": zipfile.ZIP_LZMA,
                }[compression_method_select]

                with zipfile.ZipFile("students.dat", "w", compression=compression_method) as zip_file:
                    for file_name in ["students.txt", "courses.txt", "marks.txt"]:
                        zip_file.write(file_name) if os.path.exists(file_name) else None

                for file_name in ["students.txt", "courses.txt", "marks.txt"]:
                    os.remove(file_name) if os.path.exists(file_name) else None

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
