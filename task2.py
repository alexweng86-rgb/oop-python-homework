class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def add_course(self, course):
        self.courses_attached.append(course)


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_homework(self, student, course, grade):
        if not isinstance(student, Student):
            raise TypeError('Оценку за домашнее задание может поставить только студенту')
        if course not in student.courses_in_progress:
            raise ValueError('Студент не изучает этот курс')
        if course not in self.courses_attached:
            raise ValueError('Проверяющий не закреплён за этим курсом')
        if not 1 <= grade <= 10:
            raise ValueError('Оценка должна быть по десятибалльной шкале')
        student.grades.setdefault(course, []).append(grade)


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.courses_in_progress = []
        self.finished_courses = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            raise TypeError('Оценку за лекцию может поставить только лектору')
        if course not in self.courses_in_progress:
            raise ValueError('Студент не изучает этот курс')
        if course not in lecturer.courses_attached:
            raise ValueError('Лектор не закреплён за этим курсом')
        if not 1 <= grade <= 10:
            raise ValueError('Оценка должна быть по десятибалльной шкале')
        lecturer.grades.setdefault(course, []).append(grade)


lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')

student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']

print(student.rate_lecture(lecturer, 'Python', 7))
print(student.rate_lecture(lecturer, 'Java', 8))
print(student.rate_lecture(lecturer, 'С++', 8))
print(student.rate_lecture(reviewer, 'Python', 6))

print(lecturer.grades)
