
import unittest
import csv
import os
import time
from CheckMyGrade import read_all_csv, write_all_csv

# ========================
# 🔹 STUDENT TESTS
# ========================
class TestStudentRecords(unittest.TestCase):
    def setUp(self):
        self.filename = "Student.csv"
        self.backup = "Student_backup.csv"
        if os.path.exists(self.filename):
            os.rename(self.filename, self.backup)

        self.sample_data = []
        for i in range(1000):
            self.sample_data.append({
                "StudentId": f"S{i}",
                "StudentEmail": f"student{i}@mail.com",
                "CourseId": f"C{i%10}",
                "CourseName": "TestCourse",
                "ProfessorId": "P001",
                "ProfessorEmail": "prof@mail.com",
                "Grade": "B",
                "Marks": str(i % 100)
            })
        write_all_csv(self.filename, self.sample_data[0].keys(), self.sample_data)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.backup):
            os.rename(self.backup, self.filename)

    def test_add_student(self):
        students = read_all_csv(self.filename)
        students.append({
            "StudentId": "S1001",
            "StudentEmail": "new@student.com",
            "CourseId": "C001",
            "CourseName": "Physics",
            "ProfessorId": "P002",
            "ProfessorEmail": "prof2@mail.com",
            "Grade": "A",
            "Marks": "95"
        })
        write_all_csv(self.filename, students[0].keys(), students)
        updated = read_all_csv(self.filename)
        self.assertEqual(len(updated), 1001)

    def test_sort_by_email_timing(self):
        students = read_all_csv(self.filename)
        start = time.time()
        sorted_students = sorted(students, key=lambda x: x["StudentEmail"])
        end = time.time()
        print(f"\n⏱️ Time to sort 1000 students by email: {end - start:.6f} seconds")
        self.assertEqual(len(sorted_students), 1000)

# ========================
# 🔹 COURSE TESTS
# ========================
class TestCourseRecords(unittest.TestCase):
    def setUp(self):
        self.filename = "Course.csv"
        self.backup = "Course_backup.csv"
        if os.path.exists(self.filename):
            os.rename(self.filename, self.backup)

        self.sample_data = []
        for i in range(10):
            self.sample_data.append({
                "CourseId": f"C{i}",
                "CourseName": f"Course{i}",
                "Credits": str((i % 4) + 1),
                "Description": f"Description for Course{i}"
            })
        write_all_csv(self.filename, self.sample_data[0].keys(), self.sample_data)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.backup):
            os.rename(self.backup, self.filename)

    def test_add_course(self):
        courses = read_all_csv(self.filename)
        courses.append({
            "CourseId": "C100",
            "CourseName": "NewCourse",
            "Credits": "3",
            "Description": "Newly added test course"
        })
        write_all_csv(self.filename, courses[0].keys(), courses)
        updated = read_all_csv(self.filename)
        self.assertEqual(len(updated), 11)

# ========================
# 🔹 PROFESSOR TESTS
# ========================
class TestProfessorRecords(unittest.TestCase):
    def setUp(self):
        self.filename = "Professor.csv"
        self.backup = "Professor_backup.csv"
        if os.path.exists(self.filename):
            os.rename(self.filename, self.backup)

        self.sample_data = []
        for i in range(5):
            self.sample_data.append({
                "ProfessorId": f"P{i}",
                "ProfessorName": f"Prof{i}",
                "ProfEmail": f"prof{i}@mail.com",
                "ProfRank": "Senior"
            })
        write_all_csv(self.filename, self.sample_data[0].keys(), self.sample_data)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.backup):
            os.rename(self.backup, self.filename)

    def test_modify_professor(self):
        profs = read_all_csv(self.filename)
        profs[0]["ProfRank"] = "Updated Rank"
        write_all_csv(self.filename, profs[0].keys(), profs)
        updated = read_all_csv(self.filename)
        self.assertEqual(updated[0]["ProfRank"], "Updated Rank")

# ========================
# 🚀 Run all tests
# ========================
if __name__ == "__main__":
    unittest.main()


