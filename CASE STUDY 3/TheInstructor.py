import pyodbc
from ThePerson import ThePerson
import os

def create_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER= KOUIGN-AMANN\\SQLEXPRESS02;"
        "DATABASE=LearningPlatform;"
        "Trusted_Connection=yes;"
    )

class TheInstructor(ThePerson):
    def __init__(self, instructor_id, fullname, gender, age, dateofbirth, contact, email, username, password):
        super().__init__(fullname, gender, age, dateofbirth, contact, email)
        self.instructor_id = instructor_id
        self.username = username
        self.password = password

    @classmethod
    def get_data(cls):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Instructor")
        rows = cursor.fetchall()
        instructors = [cls(instructor_id = row.Ins_ID, fullname = row.Ins_FullName, gender = row.Ins_Gender, age = row.Ins_Age, dateofbirth = row.Ins_DOB, contact = row.Ins_Contact, email = row.Ins_Email, username = row.Ins_Username, password = row.Ins_Password) for row in rows]
        cursor.close()
        conn.close()
        return instructors
        
    def display_info(self):
        os.system("cls")
        print(f"Instructor ID: {self.instructor_id}")
        print(f"Fullname: {self.fullname}")
        print(f"Gender : {self.gender}")
        print(f"Age: {self.age}")
        print(f"Date of Birth: {self.dateofbirth}")
        print(f"Contact: {self.contact}")
        print(f"Email: {self.email}")
    
    @classmethod
    def search_instructor(self):
        os.system("cls")
        instructor_ID = input("Enter Instructor ID: ")
        from_instructors = TheInstructor.get_data()
        for instructor in from_instructors:
            if str(instructor_ID) == str(instructor.instructor_id):
                instructor.display_info()
                return
        print("Instructor not found.")

    @classmethod
    def register_instructor(cls):
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
            cursor.execute("INSERT INTO Instructor(Ins_FullName, Ins_Gender, Ins_Age, Ins_DOB, Ins_Contact, Ins_Email, Ins_Username, Ins_Password) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (fullname, gender, age, dateofbirth, contact, email, username, password))
            conn.commit()
            print("Instructor registered successfully!")
        except Exception as e:
            print(f"Something went wrong {e}, Please check your input!")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def delete_instructor(cls):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try: 
            drop_ins_id = input("Enter the Instructor ID of the instructor you wish to delete: ")
            cursor.execute("SELECT * FROM Instructor WHERE Ins_ID = ?", (drop_ins_id))
            delete_instructor = cursor.fetchone()

            if delete_instructor: 
                confirmation = input(f"Are you sure you want to delete instructor {drop_ins_id} ? (Yes or No) ").strip().lower()
                if confirmation == "yes":
                    cursor.execute("DELETE FROM Instructor WHERE Ins_ID = ?", (drop_ins_id))
                    conn.commit()
                    print("Instructor deleted successfully!")
                else:
                    print("Deletion cancelled.")
            else:
                print("Instructor not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def view_profile(cls):
        os.system("cls")
        ins_ID = input("Enter your Instructor ID: ")
        from_ins = TheInstructor.get_data()
        for ins in from_ins:
            if str(ins_ID) == str(ins.ins_id):
                ins.display_info()
                return
        print("Instructor not found.")