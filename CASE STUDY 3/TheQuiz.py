import pyodbc
import os
from tabulate import tabulate

def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=KOUIGN-AMANN\\SQLEXPRESS02;"
        "DATABASE=LearningPlatform;"
        "Trusted_Connection=yes;"
    )

class TheQuiz():
    def __init__(self, quiz_id, course_id, quiz_title, quiz_desc, quiz_date):
        self.quiz_id = quiz_id
        self.course_id = course_id
        self.quiz_title = quiz_title
        self.quiz_desc = quiz_desc
        self.quiz_date = quiz_date

    @classmethod    
    def get_data(cls):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Quizzes")
            rows = cursor.fetchall()
            quizzes = [
                cls(quiz_id=row.Quiz_ID, course_id=row.Course_ID, quiz_title=row.Quiz_Title, quiz_desc=row.Quiz_Desciption, quiz_date=row.Quiz_Date)
                for row in rows
            ]
        except Exception as e:
            print(f"Error while retrieving quiz data: {e}")
            quizzes = []
        finally:
            cursor.close()
            conn.close()
        
        return quizzes
    
    def display_info(self):
        os.system("cls")
        print(f"Quiz ID: {self.quiz_id}")
        print(f"Course ID: {self.course_id}")
        print(f"Quiz Title: {self.quiz_title}")
        print(f"Quiz Description: {self.quiz_desc}")
        print(f"Quiz Date: {self.quiz_date}")

    @classmethod
    def search_quiz(cls):
        os.system("cls")
        quiz_ID = input("Enter Quiz ID: ")
        from_quiz = cls.get_data()
        for quiz in from_quiz:
            if str(quiz_ID) == str(quiz.quiz_id):
                quiz.display_info()
                return
        print("Quiz not found.")

    @classmethod
    def add_quiz(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            course_id = input("Enter Course ID: ")
            quiz_title = input("Enter Quiz Title: ")
            quiz_desc = input("Enter Quiz Description: ")
            quiz_date = input("Enter Quiz Date (YYYY-MM-DD): ")
            cursor.execute(
                "INSERT INTO Quizzes (Course_ID, Quiz_Title, Quiz_Desciption, Quiz_Date) VALUES (?, ?, ?, ?)",
                (course_id, quiz_title, quiz_desc, quiz_date)
            )
            conn.commit()
            print("Quiz added successfully!")
        except Exception as e:
            print(f"Something went wrong: {e}. Please check your input!")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def delete_quiz(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            drop_quiz_id = input("Enter the Quiz ID of the quiz you wish to delete: ")
            cursor.execute("SELECT * FROM Quizzes WHERE Quiz_ID = ?", (drop_quiz_id,))
            delete_quiz = cursor.fetchone()

            if delete_quiz:
                confirmation = input(f"Are you sure you want to delete quiz {drop_quiz_id}? (Yes or No) ").strip().lower()
                if confirmation == "yes":
                    cursor.execute("DELETE FROM Quizzes WHERE Quiz_ID = ?", (drop_quiz_id,))
                    conn.commit()
                    print("Quiz deleted successfully!")
                else:
                    print("Deletion cancelled.")
            else:
                print("Quiz not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def view_quiz(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            student_id = input("Enter your Student ID: ").strip()
            course_id = input("Enter the Course ID: ").strip()

            query = """
            SELECT 
                q.Quiz_ID, 
                q.Quiz_Title, 
                q.Quiz_Desciption, 
                q.Quiz_Date
            FROM Quizzes q
            JOIN EnrollmentCourseLog ecl ON q.Course_ID = ecl.Course_ID
            WHERE ecl.Student_ID = ? AND q.Course_ID = ?
            """
            cursor.execute(query, (student_id, course_id))
            quizzes = cursor.fetchall()

            if quizzes:
                quizzes_to_display = []
                for quiz in quizzes:
                    quizzes_to_display.append([
                        quiz.Quiz_ID,
                        quiz.Quiz_Title,
                        quiz.Quiz_Desciption,
                        quiz.Quiz_Date
                    ])
                
                headers = ["Quiz ID", "Title", "Description", "Date"]
                print(tabulate(quizzes_to_display, headers=headers, tablefmt="pretty"))
            else:
                print("No quizzes found for the provided Student ID and Course ID.")

        except Exception as e:
            print(f"An error occurred while retrieving quizzes: {e}")
        finally:
            cursor.close()
            conn.close()

