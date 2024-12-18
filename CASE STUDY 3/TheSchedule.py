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

class TheSchedule():
    def __init__(self, schedule_id, course_id, day_of_week, start_time, end_time):
        self.schedule_id = schedule_id
        self.course_id = course_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time

    @classmethod
    def get_data(cls):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Schedule")
            rows = cursor.fetchall()
            schedules = [
                cls(schedule_id=row.Schedule_ID, course_id=row.Course_ID, day_of_week=row.Day_Of_Week, start_time=row.Start_Time, end_time=row.End_Time) for row in rows]
        except Exception as e:
            print(f"Error while retrieving schedule data: {e}")
            schedules = []
        finally:
            cursor.close()
            conn.close()
        
        return schedules

    @classmethod
    def view_student_sched(cls, student_id):
        os.system("cls")
        conn = create_connection()
        cursor = conn.cursor()
        try:
            #Get the Schedule of the student
            query = """
            SELECT 
                sch.Schedule_ID,
                c.Course_Code,
                c.Course_Title,
                sch.Day_Of_Week,
                sch.Start_Time,
                sch.End_Time
            FROM dbo.EnrollmentCourseLog ecl
            JOIN dbo.Course c ON ecl.Course_ID = c.Course_ID
            JOIN dbo.Schedule sch ON c.Course_ID = sch.Course_ID
            WHERE ecl.Student_ID = ?
            ORDER BY sch.Day_Of_Week, sch.Start_Time;
            """
            cursor.execute(query, (student_id))
            
            schedule = cursor.fetchall()

            if schedule:
                schedule_to_display = []
                for sched in schedule:
                    schedule_to_display.append([sched.Schedule_ID, sched.Course_Code, sched.Course_Title, sched.Day_Of_Week, sched.Start_Time, sched.End_Time])
                
                headers = ["Schedule ID", "Course Code", "Course Title", "Day of Week", "Start Time", "End Time"]
                print(tabulate(schedule_to_display, headers=headers, tablefmt="pretty"))
            else:
                print("No schedule found for the student.")

        except Exception as e:
            print(f"An error occurred while fetching the schedule: {e}")

        finally:
            cursor.close()
            conn.close()

    @classmethod
    def view_instructor_sched(cls):
        os.system("cls")
        course_id = input("Enter Course ID: ").strip()
        
        conn = create_connection()
        cursor = conn.cursor()
        try:
            # Get the Schedule for the instructor based on course_id
            query = """
                SELECT 
                    sch.Schedule_ID,
                    c.Course_Code,
                    c.Course_Title,
                    sch.Day_Of_Week,
                    sch.Start_Time,
                    sch.End_Time
                FROM dbo.Course c
                JOIN dbo.Schedule sch ON c.Course_ID = sch.Course_ID
                WHERE c.Course_ID = ?
                ORDER BY sch.Day_Of_Week, sch.Start_Time;
            """
            cursor.execute(query, (course_id,))
            schedule = cursor.fetchall()

            if schedule:
                schedule_to_display = []
                for sched in schedule:
                    schedule_to_display.append([sched.Schedule_ID, sched.Course_Code, sched.Course_Title, sched.Day_Of_Week, sched.Start_Time, sched.End_Time])
                
                headers = ["Schedule ID", "Course Code", "Course Title", "Day of Week", "Start Time", "End Time"]
                print(tabulate(schedule_to_display, headers=headers, tablefmt="pretty"))
            else:
                print("No schedule found for this course.")

        except Exception as e:
            print(f"An error occurred while fetching the schedule: {e}")

        finally:
            cursor.close()
            conn.close()