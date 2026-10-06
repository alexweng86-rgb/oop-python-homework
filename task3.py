class AverageMixin:
    @property
    def average_grade(self):
        values = [grade for course_grades in self.grades.values() for grade in course_grades]
        if not values:
            return 0
        return round(sum(values) / len(values), 1)

    def _key(self, other):
        if not isinstance(other, self.__class__):
            return None
        return self.average_grade

    def __eq__(self, other):
        key = self._key(other)
        return NotImplemented if key is None else key == other.average_grade

    def __lt__(self, other):
        key = self._key(other)
        return NotImplemented if key is None else key < other.average_grade

    def __le__(self, other):
        key = self._key(other)
        return NotImplemented if key is None else key <= other.average_grade

    def __gt__(self, other):
        key = self._key(other)
        return NotImplemented if key is None else key > other.average_grade

    def __ge__(self, other):
        key = self._key(other)
        return NotImplemented if key is None else key >= other.average_grade


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def add_course(self, course):
        self.courses_attached.append(course)


class Lecturer(AverageMixin, Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {self.average_grade}')


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

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')


class Student(AverageMixin):
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

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {self.average_grade}\n'
                f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {", ".join(self.finished_courses)}')


some_reviewer = Reviewer('Some', 'Buddy')
some_lecturer = Lecturer('Some', 'Buddy')
some_lecturer.grades = {'Python': [10, 9, 10, 10, 10], 'Java': [10, 10, 10, 9, 10]}
some_student = Student('Ruoy', 'Eman', 'M')
some_student.courses_in_progress = ['Python', 'Git']
some_student.finished_courses = ['Введение в программирование']
some_student.grades = {'Python': [10, 9, 10, 10, 10], 'Git': [10, 10, 10, 9, 10]}

print(some_reviewer)
print()
print(some_lecturer)
print()
print(some_student)

lecturer_2 = Lecturer('Пётр', 'Петров')
lecturer_2.grades = {'Python': [8, 7, 6]}
student_2 = Student('Ольга', 'Алёхина', 'Ж')
student_2.grades = {'Python': [6, 5, 7]}

print()
print(f'Лектор 1 лучше лектора 2: {some_lecturer > lecturer_2}')
print(f'Лектор 2 лучше лектора 1: {lecturer_2 > some_lecturer}')
print(f'Лектор 1 равен лектору 1: {some_lecturer == some_lecturer}')
print(f'Студент 1 лучше студента 2: {some_student > student_2}')
try:
    some_lecturer > some_student
except TypeError as error:
    print(f'Сравнение с другим типом: {error}')
