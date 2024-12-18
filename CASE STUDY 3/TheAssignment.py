import pyodbc
import os
from tabulate import tabulate

def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= KOUIGN-AMANN\\SQLEXPRESS02;"
        "DATABASE=LearningPlatform;"
        "Trusted_Connection=yes;"
    )

class TheAssignment():
    def __init__(self, assi_id, course_id, assi_title, assi_desc, assi_due_date):
        self.assi_id = assi_id
        self.course_id = course_id
        self.assi_title = assi_title
        self.assi_desc = assi_desc
        self.assi_due_date = assi_due_date

    @classmethod    
    def get_data(cls):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Assignments")
            rows = cursor.fetchall()
            assignments = [
                cls(assi_id = row.Assignment_ID, course_id = row.Course_ID, assi_title = row.Assignment_Title, assi_desc = row.Assi_Desciption, assi_due_date = row.Due_Date) for row in rows]
        except Exception as e:
            print(f"Error while retrieving schedule data: {e}")
            assignments = []
        finally:
            cursor.close()
            conn.close()
        
        return assignments
    
    def display_info(self):
        os.system("cls")
        print(f"Assignment ID: {self.assi_id}")
        print(f"Course ID: {self.course_id}")
        print(f"Assignment Title: {self.assi_title}")
        print(f"Assignment Description: {self.assi_desc}")
        print(f"Due Date: {self.assi_due_date}")

    
    @classmethod
    def search_assi(self):
        os.system("cls")
        assi_ID = input("Enter Assignment ID: ")
        from_assi = TheAssignment.get_data()
        for assi in from_assi:
            if str(assi_ID) == str(assi.assi_id):
                assi.display_info()
                return
        print("Assignment not found.")

    @classmethod
    def add_assi(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            course_id = input("Enter Course ID: ")
            assi_title = input("Enter Assignment Title: ")
            assi_desc = input("Enter Assignment Description: ")
            assi_due_date = input("Enter Due Date: ")
            cursor.execute("INSERT INTO Assignments(Course_ID, Assignment_Title, Assignment_Desciption, Due_Date) VALUES( ?, ?, ?, ?)", (course_id, assi_title, assi_desc, assi_due_date))
            conn.commit()
            print("Assignment added successfully!")
        except Exception as e:
            print(f"Something went wrong {e}, Please check your input!")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def delete_assi(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try: 
            drop_assi_id = input("Enter the Assignment ID of the assignment you wish to delete: ")
            cursor.execute("SELECT * FROM Assignments WHERE Assignment_ID = ?", (drop_assi_id))
            delete_assi = cursor.fetchone()

            if delete_assi: 
                confirmation = input(f"Are you sure you want to delete course {drop_assi_id} ? (Yes or No) ").strip().lower()
                if confirmation == "yes":
                    cursor.execute("DELETE FROM Assignments WHERE Assignment_ID = ?", (drop_assi_id))
                    conn.commit()
                    print("Assignment deleted successfully!")
                else:
                    print("Deletion cancelled.")
            else:
                print("Assignment not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def view_assignment(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            student_id = input("Enter your Student ID: ").strip()
            course_id = input("Enter the Course ID: ").strip()

            query = """
            SELECT 
                a.Assignment_ID, 
                a.Assignment_Title, 
                a.Assi_Desciption
            FROM Assignments a
            JOIN EnrollmentCourseLog ecl ON a.Course_ID = ecl.Course_ID
            WHERE ecl.Student_ID = ? AND a.Course_ID = ?
            """
            cursor.execute(query, (student_id, course_id))
            assignments = cursor.fetchall()

            if assignments:
                assignments_to_display = []
                for assignment in assignments:
                    assignments_to_display.append([
                        assignment.Assignment_ID,
                        assignment.Assignment_Title,
                        assignment.Assi_Desciption
                    ])
                
                headers = ["Assignment ID", "Title", "Description"]
                print(tabulate(assignments_to_display, headers=headers, tablefmt="pretty"))
            else:
                print("No assignments found for the provided Student ID and Course ID.")

        except Exception as e:
            print(f"An error occurred while retrieving assignments: {e}")
        finally:
            cursor.close()
            conn.close()
