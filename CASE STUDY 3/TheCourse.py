import pyodbc
import os

def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= KOUIGN-AMANN\\SQLEXPRESS02;"
        "DATABASE=LearningPlatform;"
        "Trusted_Connection=yes;"
    )

class TheCourse():
    def __init__(self, course_id, course_code, course_title, unit_credit):
        self.course_id = course_id
        self.course_code = course_code
        self.course_title = course_title
        self.unit_credit = unit_credit 

    @classmethod
    def get_data(cls):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Course")
        rows = cursor.fetchall()
        courses = [cls(course_id = row.Course_ID, course_code = row.Course_Code, course_title = row.Course_Title, unit_credit = row.Unit_Credit)for row in rows]
        cursor.close()
        conn.close()
        return courses
    
    def display_info(self):
        os.system("cls")
        print(f"Course ID: {self.course_id}")
        print(f"Course Code: {self.course_code}")
        print(f"Course Title: {self.course_title}")
        print(f"Unit Credit: {self.unit_credit}")

    @classmethod
    def search_course(self):
        os.system("cls")
        course_ID = input("Enter Course ID: ")
        from_course = TheCourse.get_data()
        for course in from_course:
            if str(course_ID) == str(course.course_id):
                course.display_info()
                return
        print("Course not found.")

    @classmethod
    def add_course(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            course_code = input("Enter Course Code: ")
            course_title = input("Enter Course Title: ")
            unit_credit = input("Enter Unit Credit: ")
            cursor.execute("INSERT INTO Course(Course_Code, Course_Title, Unit_Credit) VALUES( ?, ?, ?)", (course_code, course_title, unit_credit))
            conn.commit()
            print("Course added successfully!")
        except Exception as e:
            print(f"Something went wrong {e}, Please check your input!")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def delete_course(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try: 
            drop_crs_id = input("Enter the Course ID of the course you wish to delete: ")
            cursor.execute("SELECT * FROM Course WHERE Course_ID = ?", (drop_crs_id))
            delete_course = cursor.fetchone()

            if delete_course: 
                confirmation = input(f"Are you sure you want to delete course {drop_crs_id} ? (Yes or No) ").strip().lower()
                if confirmation == "yes":
                    cursor.execute("DELETE FROM Course WHERE Course_ID = ?", (drop_crs_id))
                    conn.commit()
                    print("Course deleted successfully!")
                else:
                    print("Deletion cancelled.")
            else:
                print("Course not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

