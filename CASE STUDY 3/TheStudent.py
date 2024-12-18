import pyodbc
from ThePerson import ThePerson
import os
from tabulate import tabulate

def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= KOUIGN-AMANN\\SQLEXPRESS02;"
        "DATABASE=LearningPlatform;"
        "Trusted_Connection=yes;"
    )

class TheStudent(ThePerson):
    def __init__(self, student_id, fullname, gender, age, dateofbirth, contact, email, username, password):
        super().__init__(fullname, gender, age, dateofbirth, contact, email)
        self.student_id = student_id
        self.username = username
        self.password = password

    @classmethod
    def get_data(cls):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Student")
        rows = cursor.fetchall()
        students = [cls(student_id = row.Student_ID, fullname = row.Student_FullName, gender = row.Student_Gender, age = row.Student_Age, dateofbirth = row.Student_DOB, contact = row.Student_Contact, email = row.Student_Email, username = row.Student_Username, password = row.Student_Password) for row in rows]
        cursor.close()
        conn.close()
        return students

    def display_info(self):
        os.system("cls")
        print(f"Student ID: {self.student_id}")
        print(f"Fullname: {self.fullname}")
        print(f"Gender : {self.gender}")
        print(f"Age: {self.age}")
        print(f"Date of Birth: {self.dateofbirth}")
        print(f"Contact: {self.contact}")
        print(f"Email: {self.email}")
    
    @classmethod
    def search_student(self):
        os.system("cls")
        student_ID = input("Enter Student ID: ")
        from_students = TheStudent.get_data()
        for student in from_students:
            if str(student_ID) == str(student.student_id):
                student.display_info()
                return
        print("Student not found.")
    
    @classmethod
    def enroll_student(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            fullname = input("Enter fullname (Surname-First Name-Middle Initial): ")
            gender = input("Enter gender: ")
            age = input("Enter age: ")
            dateofbirth = input("Enter date of birth: ")
            contact = input("Enter contact number: ")
            email = input("Enter email address: ")
            username = input("Enter desired username: ")
            password = input("Enter password: ")
            cursor.execute("INSERT INTO Student(Student_FullName, Student_Gender, Student_Age, Student_DOB, Student_Contact, Student_Email, Student_Username, Student_Password) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (fullname, gender, age, dateofbirth, contact, email, username, password))
            conn.commit()

            cursor.execute("SELECT @@IDENTITY AS NewID")
            new_student_id = cursor.fetchone().NewID
            enrollment_date = input("Enter enrollment date: ")
            cursor.execute("INSERT INTO EnrollmentDetails(Student_ID, Enrollment_Date) VALUES(?, ?)", (new_student_id, enrollment_date))
            conn.commit()

            print("Student enrolled successfully!")
        except Exception as e:
            print(f"Something went wrong {e}, Please check your input!")
        finally:
            cursor.close()
            conn.close()
    
    @classmethod
    def delete_student(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try: 
            drop_student_id = input("Enter the Student ID of the student you wish to delete: ").strip()
            cursor.execute("SELECT * FROM EnrollmentDetails WHERE Student_ID = ?", (drop_student_id,))
            delete_student = cursor.fetchone()

            if delete_student: 
                confirmation = input(f"Are you sure you want to delete student {drop_student_id} and associated records? (Yes or No) ").strip().lower()
                if confirmation == "yes":
                    cursor.execute("DELETE FROM EnrollmentDetails WHERE Student_ID = ?", (drop_student_id,))
                    cursor.execute("DELETE FROM Student WHERE Student_ID = ?", (drop_student_id,))
                    conn.commit()
                    print("Student and associated records deleted successfully!")
                else:
                    print("Deletion cancelled.")
            else:
                print("Student not found in EnrollmentDetails.")
        except Exception as e:
            print(f"An error occurred during student deletion: {e}")
        finally:
            cursor.close()
            conn.close()

    #Student will self enroll
    def enroll_to_course(self):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        courses_to_display= []
        try:
            cursor.execute("SELECT * FROM Courses")
            courses = cursor.fetchall()
            print("Available Courses:")
            for course in courses:
                courses_to_display.append([course.course_id, course.course_code, course.course_title, course.unit_credit])
            header = ["Program ID", "Course ID", "Course Code", "Course Title", "Unit Credit"]
            print(tabulate(courses_to_display, header, tablefmt="pretty"))

            course_id = input("Enter the Course ID you want to enroll in: ").strip()

            cursor.execute("SELECT * FROM Courses WHERE Course_ID = ?", (course_id))
            course = cursor.fetchone()
            if not course:
                print(f"Course with ID {course_id} does not exist.")
                return

            cursor.execute("SELECT * FROM EnrollmentCourseLog WHERE Student_ID = ? AND Course_ID = ?", (self.student_id, course_id))
            enrollment = cursor.fetchone()
            if enrollment:
                print(f"You are already enrolled in the course: {course_id}")
                return

            enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ").strip()
            cursor.execute(
                "INSERT INTO EnrollmentCourseLog (Student_ID, Course_ID, Log_Date) VALUES (?, ?, ?)",
                (self.student_id, course_id, enrollment_date)    )
            conn.commit()
            print(f"Successfully enrolled in the course: {course.Course_Title}")

        except Exception as e:
            print(f"An error occurred during enrollment: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def view_profile(cls):
        os.system("cls")
        student_ID = input("Enter your Student ID: ")
        from_students = TheStudent.get_data()
        for student in from_students:
            if str(student_ID) == str(student.student_id):
                student.display_info()
                return
        print("Student not found.")