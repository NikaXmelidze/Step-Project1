import json
from faker import Faker
import random
import os

fake = Faker()


class Student:
    def __init__(self, name, roll_number, grade):
        self.name = name
        self.roll_number = roll_number
        self.grade = grade

    def __str__(self):
        return f"Name: {self.name}, Roll Number: {self.roll_number}, Grade: {self.grade}"


class StudentManagement:
    def __init__(self):
        self.students = []
        self.grade_char = ["A", "B", "C", "D", "E", "F"]

    # Check if JSON file is empty
    @staticmethod
    def is_json_file_empty(filename):
        return not os.path.exists(filename) or os.path.getsize(filename) == 0

    # Custom JSON encoder for Student object
    @staticmethod
    def custom_encoder(obj):
        if isinstance(obj, Student):
            return {
                "name": obj.name,
                "roll_number": obj.roll_number,
                "grade": obj.grade
            }
        return obj

    # Custom JSON decoder for Student object
    @staticmethod
    def custom_decoder(json_data):
        return Student(json_data['name'], json_data['roll_number'], json_data['grade'])

    # Write data to JSON file
    @staticmethod
    def write_data(lst):
        with open("student_data.json", "w") as json_file:
            json.dump(lst, json_file, default=StudentManagement.custom_encoder, indent=4)

    # Read data from JSON file
    @staticmethod
    def read_data():
        with open("student_data.json", "r") as read_json:
            python_data = json.load(read_json, object_hook=StudentManagement.custom_decoder)
            return python_data

    # Bubble sort by roll number
    def bubble_sort(self):
        n = len(self.students)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if self.students[j].roll_number > self.students[j + 1].roll_number:
                    self.students[j], self.students[j + 1] = self.students[j + 1], self.students[j]
        return self.students

    # Binary search by roll number
    def binary_search(self, roll_number):
        low = 0
        high = len(self.students) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.students[mid].roll_number == roll_number:
                return self.students[mid]
            elif self.students[mid].roll_number < roll_number:
                low = mid + 1
            else:
                high = mid - 1
        return None

    # Generate fake students with Faker library
    def generate_fake_students(self, num_students):
        self.students = [Student(fake.name(), random.randint(1000, 9999), random.choice(self.grade_char))
                         for _ in range(num_students)]

        self.bubble_sort()
        self.write_data(self.students)

    # Add a new student
    def add_student(self, name, roll_number, grade):
        self.students = self.read_data()
        self.students.append(Student(name, roll_number, grade.upper()))

        self.bubble_sort()
        self.write_data(self.students)
        print("Student added successfully!")

    # Display all students
    def display_students(self):
        self.students = self.read_data()
        if self.students:
            print("Added students:")
            for student in self.students:
                print(student)

    # Search for a student by roll number
    def search_student_by_roll_number(self, roll_number):
        self.students = self.read_data()

        student = self.binary_search(roll_number)
        if student:
            print("Student found:")
            print(student)
        else:
            print("Student not found")

    # Update a student's grade
    def update_student_grade(self, roll_number, new_grade):
        self.students = self.read_data()

        student = self.binary_search(roll_number)

        if student:
            student.grade = new_grade
            self.write_data(self.students)
        else:
            print("Student not found.")


def main():
    management = StudentManagement()

    # Generate fake students if JSON file is empty
    if management.is_json_file_empty("student_data.json"):
        management.generate_fake_students(10)

    while True:
        print("\nMenu:")
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student by Roll Number")
        print("4. Update Student Grade")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                try:
                    name = input("Enter student's name: ").capitalize()
                    if not name.replace(" ", "").isalpha():
                        raise ValueError("Invalid name. Name must contain only alphabets and spaces.")
                    break
                except ValueError as e:
                    print(str(e))

            while True:
                try:
                    roll_number = int(input("Enter student's roll number (1000-9999): "))
                    if not (1000 <= roll_number <= 9999):
                        raise ValueError("Invalid roll number. Roll number must be between 1000 and 9999.")
                    if management.binary_search(roll_number):
                        raise ValueError("Roll number already exists. Please enter a unique roll number.")
                    break
                except ValueError as e:
                    print(str(e))

            while True:
                try:
                    grade = input("Enter student's grade: ")
                    if grade.upper() not in ["A", "B", "C", "D", "E", "F"]:
                        raise ValueError("Invalid grade. Grade must be one of: A, B, C, D, E, F")
                    break
                except ValueError as e:
                    print(str(e))

            management.add_student(name, roll_number, grade)

        elif choice == "2":
            management.display_students()

        elif choice == "3":
            while True:
                try:
                    roll_number_to_search = int(input("Enter roll number to search for the student: "))
                    if not str(roll_number_to_search).isdigit():
                        raise ValueError("Invalid roll number. Roll number must contain only digits.")
                    break
                except ValueError as e:
                    print(str(e))

            management.search_student_by_roll_number(roll_number_to_search)

        elif choice == "4":
            while True:
                try:
                    roll_number_to_update = int(input("Enter roll number of the student to update grade: "))
                    if not str(roll_number_to_update).isdigit():
                        raise ValueError("Invalid roll number. Roll number must contain only digits.")
                    break
                except ValueError as e:
                    print(str(e))

            while True:
                try:
                    new_grade = input("Enter new grade: ")
                    if new_grade.upper() not in ["A", "B", "C", "D", "E", "F"]:
                        raise ValueError("Invalid grade. Grade must be one of: A, B, C, D, E, F")
                    break
                except ValueError as e:
                    print(str(e))

            management.update_student_grade(roll_number_to_update, new_grade)

        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == '__main__':
    main()
