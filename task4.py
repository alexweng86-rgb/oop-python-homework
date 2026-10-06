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


def average_student_grade(students, course):
    values = [grade for student in students for grade in student.grades.get(course, [])]
    if not values:
        return 0
    return round(sum(values) / len(values), 1)


def average_lecturer_grade(lecturers, course):
    values = [grade for lecturer in lecturers for grade in lecturer.grades.get(course, [])]
    if not values:
        return 0
    return round(sum(values) / len(values), 1)


lecturer_1 = Lecturer('Иван', 'Иванов')
lecturer_2 = Lecturer('Пётр', 'Петров')
reviewer_1 = Reviewer('Алексей', 'Смирнов')
reviewer_2 = Reviewer('Дмитрий', 'Иванов')
student_1 = Student('Ольга', 'Алёхина', 'Ж')
student_2 = Student('Александр', 'Сидоров', 'М')

lecturer_1.add_course('Python')
lecturer_1.add_course('Git')
lecturer_2.add_course('Python')
lecturer_2.add_course('Java')
reviewer_1.add_course('Python')
reviewer_1.add_course('Git')
reviewer_2.add_course('Python')
reviewer_2.add_course('Java')

student_1.courses_in_progress += ['Python', 'Git']
student_1.finished_courses += ['Введение в программирование']
student_2.courses_in_progress += ['Python', 'Java']
student_2.finished_courses += ['Введение в программирование']

reviewer_1.rate_homework(student_1, 'Python', 9)
reviewer_1.rate_homework(student_1, 'Python', 8)
reviewer_1.rate_homework(student_1, 'Git', 10)
reviewer_2.rate_homework(student_1, 'Python', 7)
reviewer_2.rate_homework(student_2, 'Python', 6)
reviewer_2.rate_homework(student_2, 'Python', 9)
reviewer_2.rate_homework(student_2, 'Java', 8)

student_1.rate_lecture(lecturer_1, 'Python', 10)
student_1.rate_lecture(lecturer_1, 'Python', 9)
student_1.rate_lecture(lecturer_1, 'Git', 8)
student_2.rate_lecture(lecturer_1, 'Python', 7)
student_2.rate_lecture(lecturer_2, 'Python', 9)
student_2.rate_lecture(lecturer_2, 'Java', 10)

print(lecturer_1)
print()
print(lecturer_2)
print()
print(reviewer_1)
print()
print(reviewer_2)
print()
print(student_1)
print()
print(student_2)
print()

print(f'Лектор 1 лучше лектора 2: {lecturer_1 > lecturer_2}')
print(f'Студент 1 лучше студента 2: {student_1 > student_2}')
print()

print(f'Средняя оценка студентов по Python: '
      f'{average_student_grade([student_1, student_2], "Python")}')
print(f'Средняя оценка студентов по Git: '
      f'{average_student_grade([student_1, student_2], "Git")}')
print(f'Средняя оценка лекторов по Python: '
      f'{average_lecturer_grade([lecturer_1, lecturer_2], "Python")}')
print(f'Средняя оценка лекторов по Java: '
      f'{average_lecturer_grade([lecturer_1, lecturer_2], "Java")}')
