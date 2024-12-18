from TheStudent import TheStudent
from TheEnrollmentDetails import TheEnrollmentDetails
from TheEnrollmentDetails import TheEnrollmentCourseLog
from TheInstructor import TheInstructor
from TheCourse import TheCourse
from TheSchedule import TheSchedule
from TheModule import TheModule
from TheAssignment import TheAssignment
from TheQuiz import TheQuiz
from TheGrade import TheGrade
import os
import pyodbc
import getpass
from tabulate import tabulate

def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= KOUIGN-AMANN\\SQLEXPRESS02;"
        "DATABASE=LearningPlatform;"
        "Trusted_Connection=yes;"
    )

class ELearningPlatform():
    __school_name = "SIA University"
    __founder_name = "Keandra Acosta"
    __founding_date = "11/22/2024"
    __location = "Kabacan, North Cotabato"

    def __init__(self):
        self.students = TheStudent.get_data()
        self.instructors = TheInstructor.get_data()
        self.courses = TheCourse.get_data()
        self.enrollment = TheEnrollmentDetails.get_enrollment_details()
        self.courselog = TheEnrollmentCourseLog.get_log_details()
        self.schedule = TheSchedule.get_data()
        self.module = TheModule.get_data()
        self.assignment = TheAssignment.get_data()
        self.quiz = TheQuiz.get_data()
        self.grade = TheGrade.get_data()


    #This will handle user management, especially logging in
    def user_management(self):
        user_options = { 
            "1" : self.admin_menu,
            "2" : self.instructor_menu,
            "3" : self.student_menu,
        }
        while True:
            print("== Welcome to E-Learning! ==")
            print("1. Log in as Admin")
            print("2. Log in as Instructor")
            print("3. Log in as Student")
            print("4. Exit")

            UserOptions = input("Enter your choice: ")
            if UserOptions == "4":
                break
            action = user_options.get(UserOptions)
            if action:
                action()
            else:
                print("Invalid action...")

    def admin_menu(self):
        print("=== Admin Login ===")
        username = input("Enter admin username: ").strip()
        password = getpass.getpass("Enter admin password: ").strip()
        
        # Example admin credentials for testing (replace with actual DB queries)
        if username == "admin" and password == "admin123":
            print("Admin login successful!")
            self.admin_dashboard()
        else:
            print("Invalid admin credentials.")

    def admin_dashboard(self):
        admin_menu_options = {
            "1" : self.students_menu,
            "2" : self.instructors_menu,
            "3" : self.courses_menu
        }
        while True:
            self.students = TheStudent.get_data()
            self.instructors = TheInstructor.get_data()
            print("== Please choose which to check... ==")
            print("1. Student")
            print("2. Instructor")
            print("3. Courses")
            print("4. Go Back")

            AdminOptions = input("Enter your choice: ")
            if AdminOptions == "4":
                break
            action = admin_menu_options.get(AdminOptions)
            if action:
                action()
            else:
                print("Invalid action...")
    
    #this is different from student_menu, because this is something that the admin can access to toggle with the students
    def students_menu(self):
        students_options = {
            "1" : self.search_student,
            "2" : self.display_all_students,
            "3" : self.enroll_student,
            "4" : self.delete_student,
            "5" : self.display_enrollment_details,
        }
        while True: 
            print("== Checking Student ==")
            print("1. Search Student")
            print("2. Display All Students")
            print("3. Enroll Student")
            print("4. Delete Student")
            print("5. Display Enrollment Details")
            print("6. Go Back")

            AdminStudentsChoice = input("Enter your choice: ")
            if AdminStudentsChoice == "6":
                break
            action = students_options.get(AdminStudentsChoice)
            if action:
                action()
            else: 
                print("Invalid action...")
    
    #We are calling the functions from here to the dictionary
    def search_student(self):
        TheStudent.search_student()
    def enroll_student(self):
        TheStudent.enroll_student()
    def delete_student(self):
        TheStudent.delete_student()
    @staticmethod
    def display_all_students():
        students = TheStudent.get_data()
        students_to_display= []
        for student in students:
            students_to_display.append([student.student_id, student.fullname, student.gender, student.age, student.dateofbirth, student.contact, student.email])
        header = ["ID", "Fullname", "Gender", "Age", "Date of Birth", "Contact", "Email"]
        print(tabulate(students_to_display, header, tablefmt="pretty"))

    @staticmethod
    def display_enrollment_details():
        enrolled_students = TheEnrollmentDetails.get_enrollment_details()
        display_enrollment = []
        for details in enrolled_students:
            display_enrollment.append([details.enrollment_id, details.student_id, details.enrollment_date])
        header = ["Enrollment ID", "Student ID", "Enrollment Date"]
        print(tabulate(display_enrollment, header, tablefmt="pretty"))
    
    #this is different from instructor_menu, because this is something that the admin can access to toggle with the instructors
    def instructors_menu(self):
        instructors_option = {
            "1" : self.search_instructor,
            "2" : self.display_all_instructors,
            "3" : self.register_instructor,
            "4" : self.delete_instructor,
        }
        while True: 
            print("== Checking Instructor ==")
            print("1. Search Instructor")
            print("2. Display All Instructors")
            print("3. Register Instructor")
            print("4. Delete Instructor")
            print("5. Go Back")
            AdminInsChoice = input("Enter your choice: ")
            if AdminInsChoice == "5":
                break
            action = instructors_option.get(AdminInsChoice)
            if action:
                action()
            else: 
                print("Invalid action...")

    #We are calling the functions from here to the dictionary
    def search_instructor(self):
        TheInstructor.search_instructor()
    def register_instructor(self):
        TheInstructor.register_instructor()
    def delete_instructor(self):
        TheInstructor.delete_instructor()
    @staticmethod
    def display_all_instructors():
            instructors = TheInstructor.get_data()
            ins_to_display= []
            for instructor in instructors:
                ins_to_display.append([instructor.instructor_id, instructor.fullname, instructor.gender, instructor.age, instructor.dateofbirth, instructor.contact, instructor.email])
            header = ["ID", "Fullname", "Gender", "Age", "Date of Birth", "Contact", "Email"]
            print(tabulate(ins_to_display, header, tablefmt="pretty"))

    #This is for the course menu
    def courses_menu(self):
        courses_options = {
            "1" : self.search_courses,
            "2" : self.display_all_courses,
            "3" : self.add_course,
            "4" : self.delete_course,
        }
        while True:
            print("== Checking Course ==")
            print("1. Search Course")
            print("2. Display All Courses")
            print("3. Add Course")
            print("4. Delete Course")
            print("5. Go Back")
            AdminCrsChoice = input("Enter your choice: ")
            if AdminCrsChoice == "5":
                break
            action = courses_options.get(AdminCrsChoice)
            if action:
                action()
            else: 
                print("Invalid action...")

    #Course functions
    def search_courses(self):
        TheCourse.search_course()
    def add_course (self):
        TheCourse.add_course()
    def delete_course(self):
        TheCourse.delete_course()
    @staticmethod
    def display_all_courses():
        courses = TheCourse.get_data()
        courses_to_display= []
        for course in courses:
            courses_to_display.append([course.course_id, course.course_code, course.course_title, course.unit_credit])
        header = ["Course ID", "Course Code", "Course Title", "Unit Credit"]
        print(tabulate(courses_to_display, header, tablefmt="pretty"))

    def instructor_menu(self):
        conn = None
        cursor = None
        try:
            conn = create_connection()
            cursor = conn.cursor()

            print("=== Instructor Login ===")
            username = input("Enter your username: ").strip()
            password = getpass.getpass("Enter your password: ").strip()

            cursor.execute("SELECT Ins_ID, Ins_Password FROM Instructor WHERE Ins_Username = ?", (username,))
            instructor = cursor.fetchone()

            if not instructor:
                print("Invalid username. Please try again.")
                return

            stored_password = instructor[1]
            if password == stored_password:
                print("Login successful!")
                ins_id = instructor[0]
                self.ins_dashboard(ins_id)
            else:
                print("Incorrect password. Please try again.")
                return

        except Exception as e:
            print(f"An error occurred during authentication: {e}")
            return
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    #After authentication, it will redirect to this
    def ins_dashboard(self, ins_id):
        ins_dashboard = {
            "1": self.view_profile,
            "2": self.display_students,
            "3": self.display_schedule,
            "4": self.course_dashboard_forIns
        }

        while True:
            print("=== Instructor Dashboard ===")
            print("1. View Profile")
            print("2. Display Students")
            print("3. Display Schedule")
            print("4. Course Dashboard")
            print("0. Logout")

            ins_option = input("Enter your choice: ").strip()
            if ins_option == "0":
                print("Logging out...")
                break
            action = ins_dashboard.get(ins_option)
            if action:
                action()
            else:
                print("Invalid action. Please try again.")

    def view_profile(self):
        TheInstructor.view_profile()

    @staticmethod
    def display_students():
        os.system("cls")
        course_id = input("Enter the Course ID to view enrolled students: ").strip()
        
        students = TheStudent.get_data()
        students_in_course = []

        for student in students:
            if TheEnrollmentCourseLog.is_enrolled_in_course(student.student_id, course_id):
                students_in_course.append([student.student_id, student.fullname, student.gender, student.age, student.dateofbirth, student.contact, student.email])

        if students_in_course:
            header = ["ID", "Fullname", "Gender", "Age", "Date of Birth", "Contact", "Email"]
            print(tabulate(students_in_course, header, tablefmt="pretty"))
        else:
            print("No students found for this course.")

    def display_schedule(self):
        TheSchedule.view_instructor_sched()

    def course_dashboard_forIns(self):
        while True:
            print("=== Course Dashboard ===")
            print("1. Module")
            print("2. Assignment")
            print("3. Quiz")
            print("4. Grade")
            print("0. Back")

            ins_option = input("Enter your choice: ").strip()
            if ins_option == "0":
                print("Logging out...")
                return
            elif ins_option == "1":
                self.module_actions()
            elif ins_option == "2":
                self.assignment_actions()
            elif ins_option == "3":
                self.quiz_actions()
            elif ins_option == "4":
                self.grade_actions()
            else:
                print("Invalid action. Please try again.")

    def module_actions(self):
        module_dashboard = {
            "1": self.add_module,
            "2": self.delete_module,
            "3": self.display_module,
            "4": self.search_module
        }
        self._action_selector("Module Dashboard", module_dashboard)

    def assignment_actions(self):
        assignment_dashboard = {
            "1": self.add_assignment,
            "2": self.delete_assignment,
            "3": self.display_assignment,
            "4": self.search_assignment
        }
        self._action_selector("Assignment Dashboard", assignment_dashboard)

    def quiz_actions(self):
        quiz_dashboard = {
            "1": self.add_quiz,
            "2": self.delete_quiz,
            "3": self.display_quiz,
            "4": self.search_quiz
        }
        self._action_selector("Quiz Dashboard", quiz_dashboard)

    def grade_actions(self):
        grade_dashboard = {
            "1": self.add_grade,
            "2": self.update_grade,
            "3": self.delete_grade,
            "4": self.display_grade,
            "5": self.search_grade
        }
        self._action_selector("Grade Dashboard", grade_dashboard)

    # General method to handle the action selection for all categories (module, assignment, quiz, grade)
    def _action_selector(self, dashboard_name, actions):
        while True:
            print(f"=== {dashboard_name} ===")
            print("1. Add")
            print("2. Delete")
            print("3. Display")
            print("4. Search")
            print("0. Back")

            action_option = input("Enter your choice: ").strip()
            if action_option == "0":
                return
            action = actions.get(action_option)
            if action:
                action()
            else:
                print("Invalid action. Please try again.")

    # Placeholder methods to be expanded upon
    def add_module(self):
        TheModule.add_mod()

    def delete_module(self):
        TheModule.delete_mod()

    def display_module(self):
        os.system("cls")
        course_id = input("Enter Course ID: ").strip()

        conn = create_connection()
        cursor = conn.cursor()
        try:
            query = """
                SELECT Module_ID, Course_ID, Module_Title, Module_Description
                FROM dbo.Modules
                WHERE Course_ID = ?
            """
            cursor.execute(query, (course_id,))
            modules = cursor.fetchall()

            if modules:
                modules_to_display = []
                for module in modules:
                    modules_to_display.append([module.Module_ID, module.Course_ID, module.Module_Title, module.Module_Description])

                header = ["Module ID", "Course ID", "Module Title", "Description"]
                print("=== Modules ===")
                print(tabulate(modules_to_display, headers=header, tablefmt="pretty"))
            else:
                print("No modules found for this course.")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def search_module(self):
        TheModule.search_mod()

    def add_assignment(self):
        TheAssignment.add_assi()

    def delete_assignment(self):
        TheAssignment.delete_assi()

    def display_assignment(self):
        os.system("cls")
        course_id = input("Enter Course ID: ").strip()

        conn = create_connection()
        cursor = conn.cursor()
        try:
            query = """
                SELECT Assignment_ID, Assignment_Title, Assi_Desciption, Due_Date
                FROM dbo.Assignments
                WHERE Course_ID = ?
            """
            cursor.execute(query, (course_id,))
            assignments = cursor.fetchall()

            if assignments:
                assignments_to_display = []
                for assignment in assignments:
                    assignments_to_display.append([assignment.Assignment_ID, assignment.Assignment_Title, assignment.Assi_Desciption, assignment.Due_Date])

                header = ["Assignment ID", "Assignment Title", "Description", "Due Date"]
                print("=== Assignments ===")
                print(tabulate(assignments_to_display, headers=header, tablefmt="pretty"))
            else:
                print("No assignments found for this course.")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def search_assignment(self):
        TheAssignment.search_assi()

    def add_quiz(self):
        TheQuiz.add_quiz()

    def delete_quiz(self):
        TheQuiz.delete_quiz()

    def display_quiz(self):
        os.system("cls")
        course_id = input("Enter Course ID: ").strip()

        conn = create_connection()
        cursor = conn.cursor()
        try:
            query = """
                SELECT Quiz_ID, Quiz_Title, Quiz_Desciption, Quiz_Date
                FROM dbo.Quizzes
                WHERE Course_ID = ?
            """
            cursor.execute(query, (course_id,))
            quizzes = cursor.fetchall()

            if quizzes:
                quizzes_to_display = []
                for quiz in quizzes:
                    quizzes_to_display.append([quiz.Quiz_ID, quiz.Quiz_Title, quiz.Quiz_Desciption, quiz.Quiz_Date])

                header = ["Quiz ID", "Quiz Title", "Description", "Quiz Date"]
                print("=== Quizzes ===")
                print(tabulate(quizzes_to_display, headers=header, tablefmt="pretty"))
            else:
                print("No quizzes found for this course.")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def search_quiz(self):
        TheQuiz.search_quiz()

    def add_grade(self):
        TheGrade.add_grade()

    def update_grade(self):
        TheGrade.update_grade()

    def delete_grade(self):
        TheGrade.delete_grade()

    def display_grade(self):
        os.system("cls")
        course_id = input("Enter Course ID: ").strip()

        conn = create_connection()
        cursor = conn.cursor()
        try:
            query = """
                SELECT Grade_ID, Student_ID, Grade, Grade_Date
                FROM dbo.Grades
                WHERE Course_ID = ?
            """
            cursor.execute(query, (course_id,))
            grades = cursor.fetchall()

            if grades:
                grades_to_display = []
                for grade in grades:
                    grades_to_display.append([grade.Grade_ID, grade.Student_ID, grade.Grade, grade.Grade_Date])

                header = ["Grade ID", "Student ID", "Grade", "Grade Date"]
                print("=== Grades ===")
                print(tabulate(grades_to_display, headers=header, tablefmt="pretty"))
            else:
                print("No grades found for this course.")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def search_grade(self):
        TheGrade.search_grade()


#This is for the student menu, what the student will see
    def student_menu(self):
        conn = None
        cursor = None
        try:
            conn = create_connection()
            cursor = conn.cursor()

            print("=== Student Login ===")
            username = input("Enter your username: ").strip()
            password = getpass.getpass("Enter your password: ").strip()

            cursor.execute("SELECT Student_ID, Student_Password FROM Student WHERE Student_Username = ?", (username,))
            student = cursor.fetchone()

            if not student:
                print("Invalid username. Please try again.")
                return

            stored_password = student[1]
            if password == stored_password:
                print("Login successful!")
                student_id = student[0]
                self.stud_dashboard(student_id)
            else:
                print("Incorrect password. Please try again.")
                return

        except Exception as e:
            print(f"An error occurred during authentication: {e}")
            return
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    #After authentication, it will redirect to this
    def stud_dashboard(self, student_id):
        student_dashboard = {
            "1": self.view_profile,
            "2": self.display_all_courses,
            "3": self.enroll_to_course,
            "4": lambda: self.view_course(student_id),
            "5": lambda: self.view_student_sched(student_id),
            "6": self.course_overview
        }

        while True:
            print("=== Student Dashboard ===")
            print("1. View Profile")
            print("2. Display All Courses")
            print("3. Enroll to Course")
            print("4. View Your Courses")
            print("5. View Your Schedule")
            print("6. Course Overview")
            print("0. Logout")

            student_option = input("Enter your choice: ").strip()
            if student_option == "0":
                print("Logging out...")
                break
            action = student_dashboard.get(student_option)
            if action:
                action()
            else:
                print("Invalid action. Please try again.")

    def view_profile(self):
        TheStudent.view_profile()
    @staticmethod
    def display_all_courses():
        courses = TheCourse.get_data()
        courses_to_display= []
        for course in courses:
            courses_to_display.append([course.course_id, course.course_code, course.course_title, course.unit_credit])
        header = ["Course ID", "Course Code", "Course Title", "Unit Credit"]
        print(tabulate(courses_to_display, header, tablefmt="pretty"))
    def enroll_to_course(self):
        TheEnrollmentCourseLog.enroll_to_course()

    def view_course(self, student_id):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT c.Course_ID, c.Course_Code, c.Course_Title, c.Unit_Credit FROM dbo.EnrollmentCourseLog ecl JOIN dbo.Course c ON ecl.Course_ID = c.Course_ID WHERE ecl.Student_ID = ?"
            cursor.execute(query, (student_id,))
            
            courses = cursor.fetchall()

            if courses:
                courses_to_display = []
                for course in courses:
                    courses_to_display.append([course.Course_ID, course.Course_Code, course.Course_Title, course.Unit_Credit])
                
                header = ["Course ID", "Course Code", "Course Title", "Unit Credit"]
                print(tabulate(courses_to_display, headers=header, tablefmt="pretty"))
            else:
                print("You are not enrolled in any courses.")

        except Exception as e:
            print(f"Something went wrong: {e}")

        finally:
            cursor.close()
            conn.close()

    def view_student_sched(self, student_id):
        TheSchedule.view_student_sched(student_id)
    
    def course_overview(self):
        course_overview = {
            "1": self.view_module,
            "2": self.view_assignments,
            "3": self.view_quizzes,
            "4": self.view_grades
        }

        while True:
            print("=== Course Overview ===")
            print("1. View Module")
            print("2. View Assignments")
            print("3. View Quizzes")
            print("4. View Grades")
            print("0. Back")

            student_option = input("Enter your choice: ").strip()
            if student_option == "0":
                return 
            action = course_overview.get(student_option)
            if action:
                  action()
            else:
                  print("Invalid action. Please try again.")

    def view_module(self):
        TheModule.view_module()
    def view_assignments(self):
        TheAssignment.view_assignment()
    def view_quizzes(self):
        TheQuiz.view_quiz()
    def view_grades(self):
        TheGrade.view_grade()

        


#To initialize the system
learning_platform = ELearningPlatform()
learning_platform.user_management()