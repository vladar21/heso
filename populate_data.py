from django.contrib.auth import get_user_model
from users.models import Teacher, Student
from scheduling.models import EnglishClass, Lesson, Schedule, Material
from django.utils import timezone
import random
import datetime

User = get_user_model()


def generate_schedule_dates(year=2024, month=3):
    start_date = datetime.date(year, month, random.randint(1, 7))
    end_date = datetime.date(year, month, random.randint(24, 31))
    return start_date, end_date


def generate_google_meet_link():
    return "https://meet.google.com/" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz123456789", k=10))


def create_lessons(schedule, start_hour=15, end_hour=21, lesson_duration=2):
    current_date = schedule.start_date
    while current_date <= schedule.end_date:
        if current_date.weekday() != 6:  # Skip Sundays
            start_hour = 15 if current_date.weekday() < 5 else 9  # Weekdays at 15:00, Saturday at 9:00
            start_time = datetime.datetime.combine(current_date, datetime.time(start_hour, 0, tzinfo=timezone.utc))
            end_time = start_time + datetime.timedelta(hours=lesson_duration)
            
            # Define location here before using it
            location = random.choice(['on-site', 'online'])
            
            Lesson.objects.create(
                english_class=schedule.english_class,
                title=f"Lesson on {current_date}",
                description="A detailed description of the lesson.",
                start_time=start_time,
                end_time=end_time,
                status='planned',
                google_meet_link=generate_google_meet_link(),
                location=location,
                online_meeting_link=generate_google_meet_link() if location == 'online' else ""
            )
        current_date += datetime.timedelta(days=1 if current_date.weekday() == 5 else 3)  # Next lesson in 3 days, except after Saturday


# Create teachers
teacher1 = Teacher.objects.create_user(username='teacher1', email='teacher1@example.com', password='pass123', is_teacher=True)
teacher2 = Teacher.objects.create_user(username='teacher2', email='teacher2@example.com', password='pass123', is_teacher=True)

# Create students
students = [Student.objects.create_user(username=f'student{i}', email=f'student{i}@example.com', password='pass123', is_student=True, enrollment_date=datetime.date(2024, 1, 1)) for i in range(1, 13)]

# Create classes and assign students
english_class_101 = EnglishClass.objects.create(title="English 101", description="Basic English skills", teacher=teacher1)
english_class_101.students.set(students[:3])
english_class_102 = EnglishClass.objects.create(title="English 102", description="Intermediate English skills", teacher=teacher1)
english_class_102.students.set(students[3:8])
advanced_english = EnglishClass.objects.create(title="Advanced English", description="Advanced English communication skills", teacher=teacher2)
advanced_english.students.set(students[8:])

# Create schedules
schedule_dates_101, schedule_dates_102 = generate_schedule_dates(), generate_schedule_dates()
schedule_101 = Schedule.objects.create(english_class=english_class_101, term="Spring 2024", start_date=schedule_dates_101[0], end_date=schedule_dates_101[1])
schedule_102 = Schedule.objects.create(english_class=english_class_102, term="Spring 2024", start_date=schedule_dates_102[0], end_date=schedule_dates_102[1])
# Assuming advanced English class has a different schedule
schedule_advanced_dates = generate_schedule_dates()
schedule_advanced = Schedule.objects.create(english_class=advanced_english, term="Spring 2024", start_date=schedule_advanced_dates[0], end_date=schedule_advanced_dates[1])

# Create lessons for each schedule
create_lessons(schedule_101)
create_lessons(schedule_102)
create_lessons(schedule_advanced, start_hour=9)  # Advanced English starts earlier

# Create materials
materials_titles = ["Basic Grammar Book", "Intermediate Grammar Exercises", "Advanced English Communication Skills"]
for title in materials_titles:
    material = Material.objects.create(title=title, type="book")
    material.english_class.add(english_class_101, english_class_102, advanced_english)

print("Data has been populated successfully.")
