# Python standard libraries
import datetime
import random

# Django utilities
from django.utils import timezone
from django.utils.timezone import make_aware

# Django authentication
from django.contrib.auth import get_user_model

# Local Django app imports
from scheduling.models import EnglishClass, Lesson, Schedule, Material


def create_users():
    # Creating two teachers
    teacher1 = User.objects.create_user(
        username='teacher1',
        email='teacher1@example.com',
        password='password123',
        is_teacher=True,
        is_student=False
    )
    teacher2 = User.objects.create_user(
        username='teacher2',
        email='teacher2@example.com',
        password='password123',
        is_teacher=True,
        is_student=False
    )
    
    # Creating students with a loop
    students = []
    for i in range(1, 10):
        student = User.objects.create_user(
            username=f'student{i}',
            email=f'student{i}@example.com',
            password='password123',
            is_teacher=False,
            is_student=True,
            enrollment_date=timezone.now().date()  # Assuming every student enrolls on the day this script is run
        )
        students.append(student)
    
    return teacher1, teacher2, students


# Setup User model
User = get_user_model()

# Initialize a variable to keep track of the last schedule start date
last_start_date = None

existing_materials_titles = []


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
def generate_meeting_link():
    return "https://meet.google.com/" + "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=10))


def create_materials_for_lesson(lesson):
    material_types = ['book', 'video', 'article']
    random_type = random.choice(material_types)
    global existing_materials_titles
    for _ in range(random.randint(1, 2)):
        material_title = f"Material for {lesson.title} N{random.randint(1, 100)} : {random_type}"
        while material_title in existing_materials_titles:
            material_title = f"Material for {lesson.title} N{random.randint(1, 100)}"
        material = Material.objects.create(
            title=material_title,
            type=random_type,
        )
        material.lessons.add(lesson)
        existing_materials_titles.append(material_title)


# Function to create lessons for a given class and schedule
def create_lessons_for_class(english_class, schedule, lesson_titles):
    current_date = schedule.start_date
    while current_date <= schedule.end_date:
        if current_date.weekday() < 6:  # Exclude Sundays
            start_time = make_aware(datetime.datetime.combine(current_date, datetime.time(random.choice(range(9, 17)), 0)))
            end_time = start_time + datetime.timedelta(hours=2)  # Assuming each lesson lasts 2 hours
            lesson_title = random.choice(lesson_titles)
            location = random.choice(['on-site', 'online'])
            # Generate meeting link only if location is 'online'
            meeting_link = generate_meeting_link() if location == 'online' else ""

            lesson = Lesson.objects.create(
                english_class=english_class,
                title=lesson_title,
                description=f"Description for {lesson_title}",
                start_time=start_time,
                end_time=end_time,
                location=location,
                meeting_link=meeting_link,
                status='planned'
            )
            
            create_materials_for_lesson(lesson)  # Move this line here, outside the if statement
            
            current_date += datetime.timedelta(random.choice(range(2, 4)))  # Schedule next lesson 2-3 days apart
        else:
            current_date += datetime.timedelta(days=1)  # Skip to next day if Sunday


# create superadmin
superadmin = User.objects.create_superuser(
    username='SuperAdmin',
    email='super@admin.email',
    password='heso_password'
)
# create teachers and students
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
