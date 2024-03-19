# scheduling/tests.py

import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import EnglishClass, Schedule, Lesson

User = get_user_model()


class ScheduleViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users
        cls.superuser = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        cls.teacher = User.objects.create_user('teacher', 'teacher@example.com', 'teacherpass', is_teacher=True)
        cls.student = User.objects.create_user('student', 'student@example.com', 'studentpass', is_student=True)
        # Create an English class
        cls.english_class = EnglishClass.objects.create(title="English 101", teacher=cls.teacher)
        cls.english_class.students.add(cls.student)  # Add student to the class
        # Create a schedule for the class
        cls.schedule = Schedule.objects.create(english_class=cls.english_class, term="Fall 2023", start_date=timezone.now(), end_date=timezone.now())

    def test_schedule_view_for_anonymous_user(self):
        response = self.client.get(reverse('schedule'))
        self.assertEqual(response.status_code, 200)

    def test_schedule_view_for_student(self):
        self.client.login(username='student', password='studentpass')
        response = self.client.get(reverse('schedule'))
        self.assertEqual(response.status_code, 200)

    def test_english_class_creation_by_teacher(self):
        self.client.login(username='teacher', password='teacherpass')
        response = self.client.get(reverse('create_english_class'))
        self.assertEqual(response.status_code, 200)

    def test_english_class_creation_by_student(self):
        self.client.login(username='student', password='studentpass')
        response = self.client.get(reverse('create_english_class'))
        self.assertRedirects(response, reverse('english_class_list'), status_code=302, target_status_code=302)

    def test_update_english_class_by_teacher(self):
        self.client.login(username='teacher', password='teacherpass')
        response = self.client.get(reverse('update_english_class', kwargs={'pk': self.english_class.pk}))
        self.assertEqual(response.status_code, 200)

    def test_delete_english_class_by_super_user(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('delete_english_class', kwargs={'pk': self.english_class.pk}))
        self.assertEqual(response.status_code, 200)

    def test_lesson_details_access_by_teacher(self):
        # Assuming lesson_details view exists and has a url named 'lesson_details'
        lesson = Lesson.objects.create(english_class=self.english_class, title="Lesson 1", start_time=timezone.now(), end_time=timezone.now())
        self.client.login(username='teacher', password='teacherpass')
        response = self.client.post(reverse('lesson_details'), {'lessonId': lesson.pk}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_lesson_details_access_by_student(self):
        # Simulate the student trying to access lesson details
        self.client.force_login(self.student)
        lesson = Lesson.objects.create(english_class=self.english_class, title="Lesson 1", start_time=timezone.now(), end_time=timezone.now())
        response = self.client.post(reverse('lesson_details'), data=json.dumps({'lessonId': lesson.pk}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_lesson_details_access_by_anonymous_user(self):
        lesson = Lesson.objects.create(english_class=self.english_class, title="Lesson 3", start_time=timezone.now(), end_time=timezone.now())
        response = self.client.post(reverse('lesson_details'), {'lessonId': lesson.pk}, content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['message'], 'Unauthorized access. Please log in.')
