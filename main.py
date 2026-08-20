"""
Домашняя работа по ООП:
- Вспомогательные функции расчета и валидации;
- Базовый класс Mentor;
- Дочерний класс Lecturer (Лекторы);
- Дочерний класс Reviewer (Проверяющие).

"""


def _average(values):
    """Возвращает среднее арифметическое с округлением до 1 знака."""
    values = list(values)
    if not values:
        return 0.0
    return round(sum(values) / len(values), 1)


def _is_valid_grade(grade):
    """Проверяет, что оценка находится в диапазоне от 1 до 10."""
    return (
            isinstance(grade, (int, float))
            and not isinstance(grade, bool)
            and 1 <= grade <= 10
    )


class Mentor:
    """Родительский класс для преподавателей."""

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.courses_attached = []

    def __str__(self):
        return f"Имя: {self.first_name}\nФамилия: {self.last_name}"


class Lecturer(Mentor):
    """Лектор, которому студенты ставят оценки за лекции."""

    def __init__(self, first_name, last_name):
        super().__init__(first_name, last_name)
        self.grades = {}

    @property
    def average_grade(self):
        """Средняя оценка за лекции по всем курсам."""
        all_grades = [
            grade
            for grades in self.grades.values()
            for grade in grades
        ]
        return _average(all_grades)

    def __str__(self):
        return (
            f"{super().__str__()}\n"
            f"Средняя оценка за лекции: {self.average_grade:.1f}"
        )

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade == other.average_grade

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade < other.average_grade

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade <= other.average_grade

    def __gt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade > other.average_grade

    def __ge__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade >= other.average_grade

    def __ne__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade != other.average_grade


class Reviewer(Mentor):
    """Эксперт, который проверяет домашние задания студентов."""

    def rate_hw(self, student, course, grade):
        """
        Reviewer выставляет студенту оценку за домашнее задание.
        Курс должен быть у проверяющего в courses_attached
        и у студента в courses_in_progress.
        """
        if (
                isinstance(student, Student)  # Класс Student будет объявлен в Части 2
                and course in self.courses_attached
                and course in student.courses_in_progress
                and _is_valid_grade(grade)
        ):
            student.grades.setdefault(course, []).append(grade)
            return None
        return "Ошибка"

    def rate_student(self, student, course, grade):
        """Синоним для rate_hw, если так удобнее."""
        return self.rate_hw(student, course, grade)

    def __str__(self):
        """Уникальный вывод для экспертов (задание 3)."""
        return f"Имя: {self.first_name}\nФамилия: {self.last_name}"

class Student:
    """Студент, который изучает курсы и оценивает лекции."""

    def __init__(self, first_name, last_name, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.courses_in_progress = []
        self.finished_courses = []
        self.grades = {}

    @property
    def average_grade(self):
        """Средняя оценка за домашние задания по всем курсам."""
        all_grades = [
            grade
            for grades in self.grades.values()
            for grade in grades
        ]
        return _average(all_grades)

    def rate_lecture(self, lecturer, course, grade):
        """
        Студент оценивает лекцию.
        Лектор должен быть экземпляром Lecturer,
        курс должен быть у лектора в courses_attached
        и у студента в courses_in_progress.
        """
        if (
                isinstance(lecturer, Lecturer)
                and course in lecturer.courses_attached
                and course in self.courses_in_progress
                and _is_valid_grade(grade)
        ):
            lecturer.grades.setdefault(course, []).append(grade)
            return None
        return "Ошибка"

    def __str__(self):
        return (
            f"Имя: {self.first_name}\n"
            f"Фамилия: {self.last_name}\n"
            f"Средняя оценка за домашние задания: {self.average_grade:.1f}\n"
            f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
            f"Завершенные курсы: {', '.join(self.finished_courses)}"
        )

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade == other.average_grade

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade < other.average_grade

    def __le__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade <= other.average_grade

    def __gt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade > other.average_grade

    def __ge__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade >= other.average_grade

    def __ne__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade != other.average_grade


def average_hw_grade_by_course(students, course):
    """
    Подсчёт средней оценки за домашние задания
    по всем студентам в рамках конкретного курса.
    """
    grades = []
    for student in students:
        if isinstance(student, Student):
            grades.extend(student.grades.get(course, []))
    return _average(grades)


def average_lecture_grade_by_course(lecturers, course):
    """
    Подсчёт средней оценки за лекции
    по всем лекторам в рамках конкретного курса.
    """
    grades = []
    for lecturer in lecturers:
        if isinstance(lecturer, Lecturer):
            grades.extend(lecturer.grades.get(course, []))
    return _average(grades)


def main():
    # ==========================================================
    # Задание 1. Наследование
    # ==========================================================
    print("=== Задание 1. Наследование ===")

    lecturer_1 = Lecturer("Иван", "Иванов")
    reviewer_1 = Reviewer("Пётр", "Петров")

    print(isinstance(lecturer_1, Mentor))  # True
    print(isinstance(reviewer_1, Mentor))  # True
    print(lecturer_1.courses_attached)     # []
    print(reviewer_1.courses_attached)     # []

    # ==========================================================
    # Задание 2. Атрибуты и взаимодействие классов
    # ==========================================================
    print("\n=== Задание 2. Атрибуты и взаимодействие классов ===")

    student_1 = Student("Ольга", "Алёхина", "Ж")

    student_1.courses_in_progress += ["Python", "Java"]
    student_1.finished_courses += ["Введение в программирование"]

    lecturer_1.courses_attached += ["Python", "C++"]
    reviewer_1.courses_attached += ["Python", "C++"]

    print(student_1.rate_lecture(lecturer_1, "Python", 7))  # None
    print(student_1.rate_lecture(lecturer_1, "Java", 8))    # Ошибка
    print(student_1.rate_lecture(lecturer_1, "С++", 8))     # Ошибка
    print(student_1.rate_lecture(reviewer_1, "Python", 6))  # Ошибка

    print(lecturer_1.grades)  # {'Python':}

    # ==========================================================
    # Задание 4. Создаём вторые экземпляры каждого класса
    # ==========================================================
    lecturer_2 = Lecturer("Мария", "Смирнова")
    reviewer_2 = Reviewer("Алексей", "Козлов")
    student_2 = Student("Иван", "Петров", "М")

    lecturer_2.courses_attached += ["Python", "Git"]
    reviewer_2.courses_attached += ["Python", "Git"]

    student_2.courses_in_progress += ["Python", "Git"]
    student_2.finished_courses += ["Основы программирования"]

    print("\n=== Дополнительные вызовы методов ===")
    print(student_2.rate_lecture(lecturer_2, "Python", 9))  # None
    print(student_2.rate_lecture(lecturer_2, "Git", 8))     # None

    print(reviewer_1.rate_hw(student_1, "Python", 10))      # None
    print(reviewer_1.rate_hw(student_1, "C++", 9))          # Ошибка
    print(reviewer_2.rate_hw(student_2, "Python", 8))       # None
    print(reviewer_2.rate_hw(student_2, "Git", 9))          # None

    # ==========================================================
    # Задание 3. Полиморфизм и магические методы
    # ==========================================================
    print("\n=== Задание 3. __str__ ===")

    print(reviewer_1)
    print()
    print(lecturer_1)
    print()
    print(student_1)
    print()
    print(lecturer_2)
    print()
    print(student_2)

    # Сравнение объектов (через @property без скобок)
    print("\n=== Задание 3. Сравнение объектов ===")

    print("lecturer_1 > lecturer_2:", lecturer_1 > lecturer_2)
    print("lecturer_1 == lecturer_2:", lecturer_1 == lecturer_2)
    print("lecturer_1 < lecturer_2:", lecturer_1 < lecturer_2)

    print("student_1 > student_2:", student_1 > student_2)
    print("student_1 == student_2:", student_1 == student_2)
    print("student_1 < student_2:", student_1 < student_2)

    # ==========================================================
    # Задание 4. Функции подсчёта средних оценок
    # ==========================================================
    print("\n=== Задание 4. Средние оценки по курсам ===")

    students = [student_1, student_2]
    lecturers = [lecturer_1, lecturer_2]

    print(
        "Средняя оценка студентов за домашние задания по Python:",
        average_hw_grade_by_course(students, "Python")
    )

    print(
        "Средняя оценка лекторов за лекции по Python:",
        average_lecture_grade_by_course(lecturers, "Python")
    )


if __name__ == "__main__":
    main()