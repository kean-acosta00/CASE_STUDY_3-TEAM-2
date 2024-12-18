import pyodbc
import os


def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=KOUIGN-AMANN\\SQLEXPRESS02;"
        "DATABASE=LearningPlatform;"
        "Trusted_Connection=yes;"
    )

class TheGrade:
    def __init__(self, grade_id, student_id, course_id, grade, grade_date):
        self.grade_id = grade_id
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade
        self.grade_date = grade_date

    @classmethod
    def get_data(cls):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Grades")
            rows = cursor.fetchall()
            grades = [
                cls(
                    grade_id=row.Grade_ID,
                    student_id=row.Student_ID,
                    course_id=row.Course_ID,
                    grade=row.Grade,
                    grade_date=row.Grade_Date,
                )
                for row in rows
            ]
        except Exception as e:
            print(f"Error while retrieving grade data: {e}")
            grades = []
        finally:
            cursor.close()
            conn.close()
        
        return grades

    def display_info(self):
        os.system("cls")
        print(f"Grade ID: {self.grade_id}")
        print(f"Student ID: {self.student_id}")
        print(f"Course ID: {self.course_id}")
        print(f"Grade: {self.grade:.2f}")
        print(f"Grade Date: {self.grade_date}")

    @classmethod
    def add_grade(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            student_id = input("Enter Student ID: ")
            course_id = input("Enter Course ID: ")
            grade = input("Enter Grade (e.g., 75.50): ")
            grade_date = input("Enter Grade Date (YYYY-MM-DD, press Enter for today): ")
            
            cursor.execute(
                "INSERT INTO Grades (Student_ID, Course_ID, Grade, Grade_Date) VALUES (?, ?, ?, ?)",
                (student_id, course_id, grade, grade_date)
            )
            conn.commit()
            print("Grade added successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def update_grade(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            grade_id = input("Enter Grade ID to update: ")
            new_grade = input("Enter New Grade (e.g., 85.75): ")
            
            cursor.execute(
                "UPDATE Grades SET Grade = ? WHERE Grade_ID = ?",
                (new_grade, grade_id)
            )
            conn.commit()
            print("Grade updated successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def delete_grade(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            grade_id = input("Enter Grade ID to delete: ")
            cursor.execute("SELECT * FROM Grades WHERE Grade_ID = ?", (grade_id,))
            delete_grade = cursor.fetchone()

            if delete_grade:
                confirmation = input(f"Are you sure you want to delete grade {grade_id}? (Yes or No) ").strip().lower()
                if confirmation == "yes":
                    cursor.execute("DELETE FROM Grades WHERE Grade_ID = ?", (grade_id,))
                    conn.commit()
                    print("Grade deleted successfully!")
                else:
                    print("Deletion cancelled.")
            else:
                print("Grade not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def view_grade(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            student_id = input("Enter your Student ID: ").strip()
            course_id = input("Enter the Course ID: ").strip()

            cursor.execute(
                "SELECT Grade, Grade_Date FROM Grades WHERE Student_ID = ? AND Course_ID = ?",
                (student_id, course_id)
            )
            grade = cursor.fetchone()

            if grade:
                print(f"Grade: {grade.Grade:.2f}")
                print(f"Grade Date: {grade.Grade_Date}")
            else:
                print("No grade found for the provided Student ID and Course ID.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def search_grade(self):
        os.system("cls")
        grade_id = input("Enter Grade ID or Student ID: ")
        from_grades = TheGrade.get_data()
        for grade in from_grades:
            if str(grade_id) == str(grade.grade_id) or str(grade_id) == str(grade.student_id):
                grade.display_info()
                return
        print("Grade not found.")