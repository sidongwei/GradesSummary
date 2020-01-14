import numpy as np


class Student:
    def __init__(self, info, courses, tests):
        self.id = info[0]
        self.name = info[1]
        self.courses = self.course_enroll(courses, tests)
        self.grades = self.test_grades()

    # enroll all courses that the student has taken at least one test in
    def course_enroll(self, courses, tests):
        courses_enrolled = []
        for test in tests:
            if self.id in test.marks:
                # search for this course in courses list and check if it is already enrolled
                for course in courses:
                    if test.course_id == course.id:
                        if course in courses_enrolled:  # already enrolled
                            break
                        else:
                            courses_enrolled.append(course) # enroll a new course
                            break
        return courses_enrolled

    # collect marks separately to make the code clearer (instead of doing enrollment and marks together)
    def test_grades(self):
        grades = {}
        for course in self.courses:
            course_grade = 0
            for test in course.tests:
                if self.id in test.marks:
                    course_grade += test.marks[self.id] * test.weight / 100.0
                # we guarantee the test belongs to the course, and the student must take another test in this course,
                # and all marks belong to this test is stored in it, so it must be the case the student did not
                # take this test while taking the course.
                else:
                    raise ValueError("Student" + str(self.id) + "didn't take all the tests for course" + str(course.id))
            grades[course.id] = course_grade
        return grades

    def avg_grades(self):
        return sum(self.grades.values()) / len(self.grades)

    def get_report(self):
        file = open("report_card_student_" + str(self.id), "w")
        file.write("Student Id: " + str(self.id) + ", name: " + self.name + "\n")
        file.write("Total Average:     %.2f%% \n\n" % self.avg_grades())
        for course in self.courses:
            file.write("    Course: " + course.name + ", Teacher: " + course.teacher + "\n")
            file.write("    Final Grade:     %.2f%% \n" % self.grades[course.id])
        file.close()


class Course:
    def __init__(self, info, tests):
        self.id = info[0]
        self.name = info[1]
        self.teacher = info[2]
        self.tests = self.check_tests(tests)

    def check_tests(self, tests):
        test_list = []
        total_weight = 0
        for test in tests:
            if test.course_id == self.id:       # check for all tests related to the course
                test_list.append(test)
                total_weight += test.weight
        if total_weight != 100:     # throw an error if the test weights do not add up
            raise ValueError('Total weight incorrect for course' + str(self.id))
        return test_list


class Test:
    def __init__(self, info, marks):
        self.id = info[0]
        self.course_id = info[1]
        self.weight = info[2]
        self.marks = self.check_marks(marks)    # marks is a dictionary

    # every test instance store all the marks for students taking this test
    def check_marks(self, marks):
        mark_results = {}
        for mark in marks:
            if mark.test_id == self.id:
                mark_results[mark.student_id] = mark.mark
        return mark_results


class Mark:
    def __init__(self, info):
        self.test_id = info[0]
        self.student_id = info[1]
        self.mark = info[2]


def main():
    # import marks first, as it does not depend on anything else
    marks = np.genfromtxt("marks.csv", dtype="i8, i8, f8", names=True, delimiter=",")
    mark_list = [Mark(mark) for mark in marks]

    # import tests, adding marks for all tests
    tests = np.genfromtxt("tests.csv", dtype="i8, i8, f8", names=True, delimiter=",")
    test_list = [Test(test, mark_list) for test in tests]

    # import courses, adding tests for all courses
    courses = np.genfromtxt("courses.csv", dtype="i8, U20, U20", names=True, delimiter=",")
    course_list = [Course(course, test_list) for course in courses]

    # import students, adding courses and tests to generate all information
    students = np.genfromtxt("students.csv", dtype="i8, U20", names=True, delimiter=",")
    student_list = [Student(student, course_list, test_list) for student in students]

    # generate reports for each students
    for student in student_list:
        student.get_report()


if __name__ == "__main__":
    main()
