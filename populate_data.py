from users.models import Teacher, Student
from scheduling.models import EnglishClass, Lesson, Schedule, Material
from django.utils import timezone
import random
from datetime import date


# Define a function to generate Google Meet links
def generate_google_meet_link():
    return "https://meet.google.com/" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz123456789", k=10))


# Create teachers
teacher1 = Teacher.objects.create_user(username='teacher1', email='teacher1@example.com', password='pass123', is_teacher=True)
teacher2 = Teacher.objects.create_user(username='teacher2', email='teacher2@example.com', password='pass123', is_teacher=True)

# Create students
students = [
    Student.objects.create_user(
        username=f'student{i}',
        email=f'student{i}@example.com',
        password='pass123',
        is_student=True,
        enrollment_date=date(2023, 9, 1)
    )
    for i in range(1, 13)
]

# Create classes
english_class_101 = EnglishClass.objects.create(title="English 101", description="Basic English skills", teacher=teacher1)
english_class_102 = EnglishClass.objects.create(title="English 102", description="Intermediate English", teacher=teacher1)
advanced_english = EnglishClass.objects.create(title="Advanced English", description="Advanced English skills", teacher=teacher2)

# Assign students to classes
english_class_101.students.set(students[:3])
english_class_102.students.set(students[3:8])
advanced_english.students.set(students[8:])

# Create schedules for classes
schedule_101 = Schedule.objects.create(english_class=english_class_101, term="Fall 2023", start_date=timezone.now().date(), end_date=timezone.now().date() + timezone.timedelta(days=90))
schedule_102 = Schedule.objects.create(english_class=english_class_102, term="Fall 2023", start_date=timezone.now().date(), end_date=timezone.now().date() + timezone.timedelta(days=90))
schedule_advanced = Schedule.objects.create(english_class=advanced_english, term="Fall 2023", start_date=timezone.now().date(), end_date=timezone.now().date() + timezone.timedelta(days=90))

# Create lessons
lessons = []
for english_class in [english_class_101, english_class_102, advanced_english]:
    for _ in range(5):  # Assuming 5 lessons per class
        lesson = Lesson.objects.create(
            english_class=english_class,
            title=f"Lesson {_+1}",
            description=f"Description for lesson {_+1}",
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            status=random.choice(['planned', 'completed', 'cancelled']),
            google_meet_link=generate_google_meet_link(),
            location=random.choice(['on-site', 'online']),
            online_meeting_link=generate_google_meet_link() if random.choice([True, False]) else ""
        )
        lessons.append(lesson)

# Create materials and associate them with classes and lessons
for i, lesson in enumerate(lessons, start=1):
    material = Material.objects.create(
        title=f"Material {i}",
        type=random.choice(["book", "video", "article"]),
        content=None  # Assuming content is uploaded separately or not applicable
    )
    material.english_class.add(lesson.english_class)
    material.lessons.add(lesson)

print("Data has been populated successfully.")
