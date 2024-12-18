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

class TheModule():
    def __init__(self, mod_id, course_id, mod_title, mod_desc):
        self.mod_id = mod_id
        self.course_id = course_id
        self.mod_title = mod_title
        self.mod_desc = mod_desc

    @classmethod    
    def get_data(cls):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Modules")
            rows = cursor.fetchall()
            modules = [
                cls(mod_id=row.Module_ID, course_id=row.Course_ID, mod_title=row.Module_Title, mod_desc=row.Module_Description)
                for row in rows
            ]
        except Exception as e:
            print(f"Error while retrieving module data: {e}")
            modules = []
        finally:
            cursor.close()
            conn.close()
        
        return modules
    
    def display_info(self):
        os.system("cls")
        print(f"Module ID: {self.mod_id}")
        print(f"Course ID: {self.course_id}")
        print(f"Module Title: {self.mod_title}")
        print(f"Module Description: {self.mod_desc}")

    @classmethod
    def search_mod(cls):
        os.system("cls")
        mod_ID = input("Enter Module ID: ")
        from_mod = cls.get_data()
        for mod in from_mod:
            if str(mod_ID) == str(mod.mod_id):
                mod.display_info()
                return
        print("Module not found.")

    @classmethod
    def add_mod(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            course_id = input("Enter Course ID: ")
            mod_title = input("Enter Module Title: ")
            mod_desc = input("Enter Module Description: ")
            cursor.execute(
                "INSERT INTO Modules (Course_ID, Module_Title, Module_Description) VALUES (?, ?, ?)",
                (course_id, mod_title, mod_desc)
            )
            conn.commit()
            print("Module added successfully!")
        except Exception as e:
            print(f"Something went wrong: {e}. Please check your input!")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def delete_mod(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            drop_mod_id = input("Enter the Module ID of the module you wish to delete: ")
            cursor.execute("SELECT * FROM Modules WHERE Module_ID = ?", (drop_mod_id,))
            delete_mod = cursor.fetchone()

            if delete_mod:
                confirmation = input(f"Are you sure you want to delete module {drop_mod_id}? (Yes or No) ").strip().lower()
                if confirmation == "yes":
                    cursor.execute("DELETE FROM Modules WHERE Module_ID = ?", (drop_mod_id,))
                    conn.commit()
                    print("Module deleted successfully!")
                else:
                    print("Deletion cancelled.")
            else:
                print("Module not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def view_module(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            student_id = input("Enter your Student ID: ").strip()
            course_id = input("Enter the Course ID: ").strip()

            query = """
            SELECT 
                m.Module_ID, 
                m.Module_Title, 
                m.Module_Description
            FROM Modules m
            JOIN EnrollmentCourseLog ecl ON m.Course_ID = ecl.Course_ID
            WHERE ecl.Student_ID = ? AND m.Course_ID = ?
            """
            cursor.execute(query, (student_id, course_id))
            modules = cursor.fetchall()

            if modules:
                modules_to_display = []
                for module in modules:
                    modules_to_display.append([
                        module.Module_ID,
                        module.Module_Title,
                        module.Module_Description
                    ])
                
                headers = ["Module ID", "Title", "Description"]
                print(tabulate(modules_to_display, headers=headers, tablefmt="pretty"))
            else:
                print("No modules found for the provided Student ID and Course ID.")

        except Exception as e:
            print(f"An error occurred while retrieving modules: {e}")
        finally:
            cursor.close()
            conn.close()