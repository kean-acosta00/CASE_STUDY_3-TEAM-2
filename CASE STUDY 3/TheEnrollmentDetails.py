import pyodbc
import os

def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= KOUIGN-AMANN\\SQLEXPRESS02;"
        "DATABASE=LearningPlatform;"
        "Trusted_Connection=yes;"
    )

class TheEnrollmentDetails():
    def __init__(self, enrollment_id, student_id, enrollment_date):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.enrollment_date = enrollment_date

    #This method is retrieving data from the EnrollmentDetails table, needed for fetching the table for EnrollmentDetails
    @classmethod
    def get_enrollment_details(cls):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM EnrollmentDetails")
        rows = cursor.fetchall()
        enrolled_students = [cls(enrollment_id = row.Enrollment_ID, student_id = row.Student_ID, enrollment_date = row.Enrollment_Date) for row in rows]
        cursor.close()
        conn.close()
        return enrolled_students
    
class TheEnrollmentCourseLog():
    def __init__(self, log_id, student_id, course_id, log_date):
        self.log_id = log_id
        self.student_id = student_id
        self.course_id = course_id
        self.log_date = log_date

    @classmethod
    def get_log_details(cls):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM EnrollmentCourseLog")
        rows = cursor.fetchall()
        enrolled_course = [cls(log_id = row.Log_ID, student_id = row.Student_ID, course_id = row.Course_ID, log_date = row.Log_Date) for row in rows]
        cursor.close()
        conn.close()
        return enrolled_course
        
    @classmethod
    def enroll_to_course(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT @@IDENTITY AS NewID")
            new_log_id = cursor.fetchone().NewID
            student_id= input("Enter you student ID: ")
            course_id = input("Enter the course ID that you want to enroll in: ")
            log_date = input("Enter enrollment date: ")
            cursor.execute("INSERT INTO EnrollmentCourseLog(Student_ID, Course_ID, Log_Date) VALUES(?, ?, ?)", (student_id, course_id, log_date))
            conn.commit()

            cursor.execute("SELECT @@IDENTITY AS NewID")
            new_sched_id = cursor.fetchone().NewID
            day_of_week = input("Enter your desired day of week: ")
            start_time = input("Enter the time you want to start: ")
            end_time = input("Enter the time you want to end: ")
            cursor.execute("INSERT INTO Schedule(Course_ID, Day_Of_Week, Start_Time, End_Time) VALUES(?,?,?,?)", (course_id, day_of_week, start_time, end_time))
            conn.commit()

            print("You are enrolled successfully!")
        except Exception as e:
            print(f"Something went wrong {e}, Please check your input!")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def is_enrolled_in_course(student_id, course_id):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM dbo.EnrollmentCourseLog WHERE Student_ID = ? AND Course_ID = ?"
            cursor.execute(query, (student_id, course_id))
            result = cursor.fetchone()

            return result is not None  # Return True if student is enrolled, False otherwise

        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()