
import csv
import os
import hashlib
import statistics
import time
from getpass import getpass

# ------------------ CSV Helpers ------------------
def read_all_csv(filename):
    rows = []
    if os.path.exists(filename):
        with open(filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)
    return rows

def write_all_csv(filename, fieldnames, rows):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def append_to_csv(filename, row_dict):
    write_header = not os.path.exists(filename) or os.stat(filename).st_size == 0
    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=row_dict.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(row_dict)

# ------------------ Safe Input ------------------
def safe_input(prompt_text, allow_exit=True, allow_back=False):
    value = input(prompt_text).strip().lower()
    if allow_exit and value == 'exit':
        print("👋 Exiting CheckMyGrade.")
        exit()
    if allow_back and value == 'back':
        return 'BACK'
    return value

# ------------------ Password Helpers ------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(input_password, stored_hash):
    return hash_password(input_password) == stored_hash

def change_password(email):
    users = read_all_csv("Login.csv")
    for u in users:
        if u["Email"] == email:
            current = input("Enter current password: ")
            if not check_password(current, u["PasswordHash"]):
                print("❌ Current password incorrect.")
                return
            new_pwd = input("Enter new password: ")
            confirm = input("Confirm new password: ")
            if new_pwd != confirm:
                print("❌ Passwords do not match.")
                return
            u["PasswordHash"] = hash_password(new_pwd)
            write_all_csv("Login.csv", users[0].keys(), users)
            print("✅ Password changed successfully.")
            return
    print("❌ User not found.")

# ------------------ Search with Timing ------------------
def search_student_by_id():
    students = read_all_csv("Student.csv")
    sid = input("Enter Student ID to search: ")

    start = time.time()
    for s in students:
        if s["StudentId"] == sid:
            print("Student Found:")
            for k, v in s.items():
                print(f"{k}: {v}")
            break
    else:
        print("Student not found.")
    end = time.time()
    print(f"⏱️ Search completed in {end - start:.6f} seconds.")

def search_professor_by_email():
    professors = read_all_csv("Professor.csv")
    email = input("Enter Professor Email to search: ")

    start = time.time()
    for p in professors:
        if p["ProfEmail"] == email:
            print("Professor Found:")
            for k, v in p.items():
                print(f"{k}: {v}")
            break
    else:
        print("Professor not found.")
    end = time.time()
    print(f"⏱️ Search completed in {end - start:.6f} seconds.")

def search_course_by_id():
    courses = read_all_csv("Course.csv")
    cid = input("Enter Course ID to search: ")

    start = time.time()
    for c in courses:
        if c["CourseId"] == cid:
            print("Course Found:")
            for k, v in c.items():
                print(f"{k}: {v}")
            break
    else:
        print("Course not found.")
    end = time.time()
    print(f"⏱️ Search completed in {end - start:.6f} seconds.")

def search_menu():
    while True:
        print("\n--- Search Menu ---")
        print("1. Search Student by ID")
        print("2. Search Professor by Email")
        print("3. Search Course by ID")
        print("0. Back")
        choice = safe_input("Enter your choice: ", allow_exit=True, allow_back=True)

        if choice == "1":
            search_student_by_id()
        elif choice == "2":
            search_professor_by_email()
        elif choice == "3":
            search_course_by_id()
        elif choice in ["0", "back"]:
            break
        else:
            print("❌ Invalid choice.")

# ------------------ Grade Helper ------------------
def calculate_grade(marks):
    marks = int(marks)
    if marks >= 90: return 'A+'
    elif marks >= 80: return 'A'
    elif marks >= 70: return 'B+'
    elif marks >= 60: return 'B'
    elif marks >= 50: return 'C'
    elif marks >= 40: return 'D'
    else: return 'F'

# ------------------ Admin Functions ------------------
def add_student():
    sid = input("Student ID: ")
    semail = input("Student Email: ")
    cid = input("Course ID: ")
    cname = input("Course Name: ")
    pid = input("Professor ID: ")
    pemail = input("Professor Email: ")
    marks = "0"
    grade = calculate_grade(marks)

    students = read_all_csv("Student.csv")
    for s in students:
        if s["StudentId"] == sid:
            print("Student ID already exists.")
            return

    row = {
        "StudentId": sid, "StudentEmail": semail,
        "CourseId": cid, "CourseName": cname,
        "ProfessorId": pid, "ProfessorEmail": pemail,
        "Grade": grade, "Marks": marks
    }
    append_to_csv("Student.csv", row)
    append_to_csv("Login.csv", {"Email": semail, "PasswordHash": "", "Role": "Student"})
    print("Student added.")

def delete_student():
    sid = input("Enter Student ID to delete: ")
    students = read_all_csv("Student.csv")
    new_students = [s for s in students if s["StudentId"] != sid]
    if len(new_students) == len(students):
        print("Student not found.")
        return
    write_all_csv("Student.csv", students[0].keys(), new_students)
    print("Student deleted.")

def modify_student():
    sid = input("Enter Student ID to modify: ")
    students = read_all_csv("Student.csv")
    found = False
    for student in students:
        if student["StudentId"] == sid:
            found = True
            for field in ["StudentEmail", "CourseId", "CourseName", "ProfessorId", "ProfessorEmail"]:
                val = input(f"{field} ({student[field]}): ")
                if val:
                    student[field] = val
            break
    if not found:
        print("Student not found.")
        return
    write_all_csv("Student.csv", students[0].keys(), students)
    print("Student updated.")

def add_professor():
    pid = input("Professor ID: ")
    pemail = input("Professor Email: ")
    pname = input("Professor Name: ")
    prank = input("Professor Rank: ")
    cid = input("Course ID: ")

    professors = read_all_csv("Professor.csv")
    for p in professors:
        if p["ProfessorId"] == pid:
            print("Professor ID already exists.")
            return

    row = {
        "ProfessorId": pid, "ProfEmail": pemail,
        "ProfessorName": pname, "ProfRank": prank,
        "CourseId": cid
    }
    append_to_csv("Professor.csv", row)
    append_to_csv("Login.csv", {"Email": pemail, "PasswordHash": "", "Role": "Professor"})
    print("Professor added.")

def delete_professor():
    pid = input("Enter Professor ID to delete: ")
    profs = read_all_csv("Professor.csv")
    new_profs = [p for p in profs if p["ProfessorId"] != pid]
    if len(new_profs) == len(profs):
        print("Professor not found.")
        return
    write_all_csv("Professor.csv", profs[0].keys(), new_profs)
    print("Professor deleted.")

def modify_professor():
    pid = input("Enter Professor ID to modify: ")
    profs = read_all_csv("Professor.csv")
    found = False
    for prof in profs:
        if prof["ProfessorId"] == pid:
            found = True
            for field in ["ProfEmail", "ProfessorName", "ProfRank", "CourseId"]:
                val = input(f"{field} ({prof[field]}): ")
                if val:
                    prof[field] = val
            break
    if not found:
        print("Professor not found.")
        return
    write_all_csv("Professor.csv", profs[0].keys(), profs)
    print("Professor updated.")

def add_course():
    cid = input("Course ID: ")
    cname = input("Course Name: ")
    credits = input("Credits: ")
    desc = input("Description: ")
    sid = input("Student ID: ")
    pid = input("Professor ID: ")

    courses = read_all_csv("Course.csv")
    for c in courses:
        if c["CourseId"] == cid:
            print("Course ID already exists.")
            return

    row = {
        "CourseId": cid, "CourseName": cname,
        "Credits": credits, "Description": desc,
        "StudentId": sid, "ProfessorId": pid
    }
    append_to_csv("Course.csv", row)
    print("Course added.")

def delete_course():
    cid = input("Enter Course ID to delete: ")
    courses = read_all_csv("Course.csv")
    new_courses = [c for c in courses if c["CourseId"] != cid]
    if len(new_courses) == len(courses):
        print("Course not found.")
        return
    write_all_csv("Course.csv", courses[0].keys(), new_courses)
    print("Course deleted.")

def modify_course():
    cid = input("Enter Course ID to modify: ")
    courses = read_all_csv("Course.csv")
    found = False
    for course in courses:
        if course["CourseId"] == cid:
            found = True
            for field in ["CourseName", "Credits", "Description", "StudentId", "ProfessorId"]:
                val = input(f"{field} ({course[field]}): ")
                if val:
                    course[field] = val
            break
    if not found:
        print("Course not found.")
        return
    write_all_csv("Course.csv", courses[0].keys(), courses)
    print("Course updated.")

# ------------------ Professor Functions ------------------
def professor_menu(current_email):
    while True:
        print("\n--- Professor Menu ---")
        print("1. View My Details")
        print("2. Add Marks for Student")
        print("3. Delete Marks for Student")
        print("4. Modify Marks for Student")
        print("5. View Reports")
        print("6. Change Password")
        print("7. Search Records")
        print("0. Logout")
        choice = safe_input("Enter choice: ", allow_exit=True, allow_back=True)

        if choice == "1":
            view_professor_details(current_email)
        elif choice == "2":
            add_marks(current_email)
        elif choice == "3":
            delete_marks(current_email)
        elif choice == "4":
            modify_marks(current_email)
        elif choice == "5":
            view_reports()
        elif choice == "6":
            change_password(current_email)
        elif choice == "7":
            search_menu()
        elif choice in ["0", "back"]:
            break

def view_professor_details(email):
    profs = read_all_csv("Professor.csv")
    for p in profs:
        if p["ProfEmail"] == email:
            for key, val in p.items():
                print(f"{key}: {val}")
            return
    print("Profile not found.")

def add_marks(prof_email):
    sid = input("Enter Student ID: ")
    students = read_all_csv("Student.csv")
    for s in students:
        if s["StudentId"] == sid and s["ProfessorEmail"] == prof_email:
            marks = input("Enter Marks: ")
            s["Marks"] = marks
            s["Grade"] = calculate_grade(marks)
            write_all_csv("Student.csv", students[0].keys(), students)
            print("Marks updated.")
            return
    print("Unauthorized or student not found.")

def delete_marks(prof_email):
    sid = input("Enter Student ID: ")
    students = read_all_csv("Student.csv")
    for s in students:
        if s["StudentId"] == sid and s["ProfessorEmail"] == prof_email:
            s["Marks"] = "0"
            s["Grade"] = calculate_grade(0)
            write_all_csv("Student.csv", students[0].keys(), students)
            print("Marks reset to 0.")
            return
    print("Unauthorized or student not found.")

def modify_marks(prof_email):
    add_marks(prof_email)

# ------------------ Student Functions ------------------
def student_menu(current_email):
    while True:
        print("\n--- Student Menu ---")
        print("1. View My Details")
        print("2. View Reports")
        print("3. Change Password")
        print("4. Search Records")
        print("0. Logout")
        choice = safe_input("Enter choice: ", allow_exit=True, allow_back=True)

        if choice == "1":
            view_student_details(current_email)
        elif choice == "2":
            view_reports()
        elif choice == "3":
            change_password(current_email)
        elif choice == "4":
            search_menu()
        elif choice in ["0", "back"]:
            break

def view_student_details(email):
    students = read_all_csv("Student.csv")
    for s in students:
        if s["StudentEmail"] == email:
            for key, val in s.items():
                print(f"{key}: {val}")
            return
    print("Student record not found.")

# ------------------ Report Functions ------------------
def view_reports():
    while True:
        print("\n--- Reports ---")
        print("1. Grades Report (sorted by Grade)")
        print("2. Grades Report (sorted by Student Name)")
        print("3. Avg & Median Scores Course-wise")
        print("4. All Professors Report")
        print("5. All Students Report")
        print("6. All Courses Report")
        print("0. Back")
        choice = safe_input("Enter your choice: ", allow_exit=True, allow_back=True)

        if choice == "1":
            grades_sorted_by_grade()
        elif choice == "2":
            grades_sorted_by_student()
        elif choice == "3":
            average_median_scores()
        elif choice == "4":
            all_professors_sorted()
        elif choice == "5":
            all_students_sorted()
        elif choice == "6":
            all_courses_sorted()
        elif choice in ['0', 'back']:
            break

def grades_sorted_by_grade():
    course = input("Enter Course ID: ")
    data = [s for s in read_all_csv("Student.csv") if s["CourseId"] == course]
    sorted_data = sorted(data, key=lambda x: x["Grade"])

    print(f"\n📊 Grades Report for Course {course} (Sorted by Grade):")
    print(f"{'StudentId':<10} | {'StudentEmail':<25} | {'Grade':<5} | Marks")
    print("-" * 60)

    for s in sorted_data:
        print(f"{s['StudentId']:<10} | {s['StudentEmail']:<25} | {s['Grade']:<5} | {s['Marks']}")

def grades_sorted_by_student():
    course = input("Enter Course ID: ")
    data = [s for s in read_all_csv("Student.csv") if s["CourseId"] == course]
    sorted_data = sorted(data, key=lambda x: x["StudentEmail"])

    print(f"\n📊 Grades Report for Course {course} (Sorted by Student Email):")
    print(f"{'StudentEmail':<25} | {'Grade':<5} | Marks")
    print("-" * 45)

    for s in sorted_data:
        print(f"{s['StudentEmail']:<25} | {s['Grade']:<5} | {s['Marks']}")

def average_median_scores():
    data = read_all_csv("Student.csv")
    course_marks = {}

    for s in data:
        course = s["CourseId"]
        try:
            mark = int(s["Marks"])
        except:
            mark = 0
        course_marks.setdefault(course, []).append(mark)

    print("\n📈 Average & Median Scores Course-Wise")
    print(f"{'CourseId':<10} | {'Average':<7} | Median")
    print("-" * 35)

    for cid, marks in course_marks.items():
        avg = sum(marks) / len(marks)
        med = statistics.median(marks)
        print(f"{cid:<10} | {avg:<7.2f} | {med:.2f}")

def all_professors_sorted():
    data = sorted(read_all_csv("Professor.csv"), key=lambda x: x["ProfessorName"])

    print("\n👨‍🏫 All Professors Report:")
    print(f"{'ProfId':<10} | {'Name':<20} | {'Email':<25} | Rank")
    print("-" * 70)

    for p in data:
        print(f"{p['ProfessorId']:<10} | {p['ProfessorName']:<20} | {p['ProfEmail']:<25} | {p['ProfRank']}")

def all_students_sorted():
    data = sorted(read_all_csv("Student.csv"), key=lambda x: x["StudentEmail"])

    print("\n🎓 All Students Report:")
    print(f"{'StudentId':<10} | {'Email':<25} | {'CourseId':<10} | Grade | Marks")
    print("-" * 70)

    for s in data:
        print(f"{s['StudentId']:<10} | {s['StudentEmail']:<25} | {s['CourseId']:<10} | {s['Grade']}   | {s['Marks']}")

def all_courses_sorted():
    data = sorted(read_all_csv("Course.csv"), key=lambda x: x["CourseName"])

    print("\n📘 All Courses Report:")
    print(f"{'CourseId':<10} | {'CourseName':<20} | {'Credits':<7} | Description")
    print("-" * 70)

    for c in data:
        print(f"{c['CourseId']:<10} | {c['CourseName']:<20} | {c['Credits']:<7} | {c['Description']}")

# ------------------ Login System & Main Menu ------------------
def ensure_admin_account():
    if not os.path.exists("Login.csv"):
        with open("Login.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Email", "PasswordHash", "Role"])
            writer.writeheader()
            writer.writerow({
                "Email": "admin@gmail.com",
                "PasswordHash": hash_password("admin"),
                "Role": "Admin"
            })

def login(expected_role):
    email = safe_input(f"Enter your {expected_role.lower()} email (or type 'exit'): ", allow_exit=True)
    if email.lower() == 'exit':
        return None, "exit"

    users = read_all_csv("Login.csv")
    for user in users:
        if user["Email"] == email:
            if user["Role"] != expected_role:
                print(f"❌ This email is not registered as a {expected_role}.")
                return None, None
            if user["PasswordHash"] == "":
                pwd = input("Set new password: ")
                user["PasswordHash"] = hash_password(pwd)
                write_all_csv("Login.csv", users[0].keys(), users)
                print("✅ Password set. Please login again.")
                return None, None
            pwd = input("Enter password: ")
            if check_password(pwd, user["PasswordHash"]):
                print("✅ Login successful.")
                return email, expected_role
            else:
                print("❌ Wrong password.")
                return None, None
    print("❌ Email not found.")
    return None, None

def main():
    ensure_admin_account()

    while True:
        print("\n--- Welcome to CheckMyGrade App ---")
        print("Please select your role:")
        print("1. Admin")
        print("2. Professor")
        print("3. Student")
        print("0. Exit")

        role_choice = safe_input("Enter your choice: ", allow_exit=True)

        if role_choice == "0":
            print("👋 Exiting CheckMyGrade. Goodbye!")
            break
        elif role_choice == "1":
            role = "Admin"
        elif role_choice == "2":
            role = "Professor"
        elif role_choice == "3":
            role = "Student"
        else:
            print("❌ Invalid option. Try again.")
            continue

        email, returned_role = login(expected_role=role)
        if returned_role != role:
            print("❌ Role mismatch or login failed.")
            continue

        if not role:
            continue
        if role == "Admin":
            while True:
                print("\n--- Admin Menu ---")
                print("1. Add Student")
                print("2. Delete Student")
                print("3. Modify Student")
                print("4. Add Professor")
                print("5. Delete Professor")
                print("6. Modify Professor")
                print("7. Add Course")
                print("8. Delete Course")
                print("9. Modify Course")
                print("10. View Reports")
                print("11. Change Password")
                print("12. Search Records")
                print("0. Logout")
                ch = safe_input("Enter choice: ", allow_exit=True, allow_back=True)
                if ch == "1": add_student()
                elif ch == "2": delete_student()
                elif ch == "3": modify_student()
                elif ch == "4": add_professor()
                elif ch == "5": delete_professor()
                elif ch == "6": modify_professor()
                elif ch == "7": add_course()
                elif ch == "8": delete_course()
                elif ch == "9": modify_course()
                elif ch == "10": view_reports()
                elif ch == "11": change_password(email)
                elif ch == "12": search_menu()
                elif ch in ["0", "back"]:
                    break
                else: print("❌ Invalid choice")
        elif role == "Professor":
            professor_menu(email)
        elif role == "Student":
            student_menu(email)
        else:
            print("❌ Unknown role.")

        # Ask if the user wants to exit the app
        retries = 3
        while retries > 0:
            exit_choice = input("Do you want to exit the app? (yes/no): ").strip().lower()
            if exit_choice in ['yes', 'y']:
                print("👋 Exiting CheckMyGrade. Goodbye!")
                break
            elif exit_choice in ['no', 'n']:
                print("🔁 Returning to login screen...\n")
                break
            else:
                retries -= 1
                print(f"❌ Invalid input. Please type 'yes' or 'no'. Attempts left: {retries}")

        if retries == 0:
            print("⚠️ Too many invalid attempts. Exiting by default.")
        break

if __name__ == "__main__":
    main()
