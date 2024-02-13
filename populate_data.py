from django.contrib.auth import get_user_model
from users.models import Teacher, Student
from scheduling.models import EnglishClass, Lesson, Schedule, Material
from django.utils.timezone import make_aware
import random
import datetime

# Setup User model
User = get_user_model()

# Initialize a variable to keep track of the last schedule start date
last_start_date = None


# Generate dates for the schedules with staggered start dates
def generate_schedule_dates(year=2024, month=3, last_date=None):
    global last_start_date
    if last_date:
        start_date = last_date + datetime.timedelta(days=random.randint(1, 3))  # Stagger start dates
    else:
        start_date = datetime.date(year, month, random.randint(1, 3))
    end_date = start_date + datetime.timedelta(days=random.randint(28, 30))  # Ensure the schedule lasts a certain period
    last_start_date = start_date  # Update the last start date
    return start_date, end_date


# Generate a random Google Meet link
def generate_google_meet_link():
    return "https://meet.google.com/" + "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=10))


def create_materials_for_lesson(lesson):
    material_types = ['book', 'video', 'article']
    for _ in range(random.randint(1, 3)):  # Each lesson can have between 1 to 3 materials
        material = Material.objects.create(
            title=f"Material for {lesson.title}",
            type=random.choice(material_types),
            # content=None,  Assuming content is uploaded separately or not applicable
        )
        # Assuming Material model has a many-to-many field with EnglishClass named 'english_classes'
        material.english_class.add(lesson.english_class)
        # If the lessons field is a ManyToMany field in Material model to associate with Lesson
        material.lessons.add(lesson)


# Function to create lessons for a given class and schedule
def create_lessons_for_class(english_class, schedule, lesson_titles):
    current_date = schedule.start_date
    while current_date <= schedule.end_date:
        if current_date.weekday() < 6:  # Exclude Sundays
            start_time = make_aware(datetime.datetime.combine(current_date, datetime.time(random.choice(range(9, 17)), 0)))
            end_time = start_time + datetime.timedelta(hours=2)  # Assuming each lesson lasts 2 hours
            lesson_title = random.choice(lesson_titles)
            lesson = Lesson.objects.create(
                english_class=english_class,
                title=lesson_title,
                description=f"Description for {lesson_title}",
                start_time=start_time,
                end_time=end_time,
                google_meet_link=generate_google_meet_link(),
                location=random.choice(['on-site', 'online']),
                status='planned'
            )
            create_materials_for_lesson(lesson)
            current_date += datetime.timedelta(random.choice(range(2, 4)))  # Schedule next lesson 2-3 days apart
        else:
            current_date += datetime.timedelta(days=1)  # Skip to next day if Sunday


# Create users, teachers, and students
def create_users():
    teacher1 = Teacher.objects.create_user(username='teacher1', email='teacher1@example.com', password='password123', is_teacher=True)
    teacher2 = Teacher.objects.create_user(username='teacher2', email='teacher2@example.com', password='password123', is_teacher=True)
    students = [Student.objects.create_user(username=f'student{i}', email=f'student{i}@example.com', password='password123', is_student=True, enrollment_date=datetime.date.today()) for i in range(1, 16)]
    return teacher1, teacher2, students


teacher1, teacher2, students = create_users()

# Define classes
classes_info = [
    ("English 101", teacher1, ["Alphabet and Phonics", "Basic Grammar", "Simple Conversations"]),
    ("English 102", teacher2, ["Intermediate Grammar", "Writing Skills", "Speaking and Listening"]),
    ("Advanced English", teacher1, ["Advanced Grammar", "Business English", "Literature"])
]

# When creating schedules for each class, use the updated function with the last_date parameter
for class_title, teacher, lesson_titles in classes_info:
    english_class = EnglishClass.objects.create(title=class_title, description=f"{class_title} Description", teacher=teacher)
    # Randomly assign students to this class
    english_class.students.set(random.sample(list(students), k=random.randint(5, len(students) // 3)))
    start_date, end_date = generate_schedule_dates(last_date=last_start_date)  # Use the last_start_date to generate new dates
    schedule = Schedule.objects.create(english_class=english_class, term="Spring 2024", start_date=start_date, end_date=end_date)
    create_lessons_for_class(english_class, schedule, lesson_titles)

print("Data population is complete.")
