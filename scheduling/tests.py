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
        self.assertRedirects(response, reverse('english_class_list'), status_code=302, target_status_code=200)

    def test_update_english_class_by_teacher(self):
        self.client.login(username='teacher', password='teacherpass')
        response = self.client.get(reverse('update_english_class', kwargs={'pk': self.english_class.pk}))
        self.assertEqual(response.status_code, 200)

    def test_delete_english_class_by_super_user(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('delete_english_class', kwargs={'pk': self.english_class.pk}))
        self.assertEqual(response.status_code, 200)

    def test_delete_english_class_by_teacher(self):
        self.client.login(username='teacher', password='teacherpass')
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

    def test_lesson_update_by_teacher(self):
        self.client.login(username='teacher', password='teacherpass')
        lesson = Lesson.objects.create(
            english_class=self.english_class, 
            title="Lesson Test", 
            start_time=timezone.now(), 
            end_time=timezone.now()
        )
        response = self.client.get(reverse('update_lesson_view', kwargs={'pk': lesson.pk}))
        self.assertEqual(response.status_code, 200)

    def test_lesson_deletion_by_superuser(self):
        self.client.login(username='admin', password='adminpass')
        lesson = Lesson.objects.create(
            english_class=self.english_class, 
            title="Lesson Deletion Test", 
            start_time=timezone.now(), 
            end_time=timezone.now()
        )
        response = self.client.get(reverse('delete_lesson', kwargs={'pk': lesson.pk}))
        self.assertEqual(response.status_code, 200)

    def test_create_english_class_by_teacher(self):
        self.client.login(username='teacher', password='teacherpass')

        classes_count_before = EnglishClass.objects.count()

        response = self.client.post(reverse('create_english_class'), data={
            'title': 'Advanced English',
            'description': 'This is an advanced English class for testing.',
            'color': '#FFD700',
            'teacher': self.teacher.id,
            'term': 'Fall 2023',
            'start_date': '2023-09-01',
            'end_date': '2023-12-31',
        })

        self.assertEqual(response.status_code, 302, f"Expected Redirect to english_class_list, got {response.status_code} instead. Form errors: {response.context['form'].errors if response.context else 'N/A'}")

        classes_count_after = EnglishClass.objects.count()
        self.assertEqual(classes_count_after, classes_count_before + 1, "A new class should have been created.")

        new_class = EnglishClass.objects.latest('id')
        self.assertEqual(new_class.teacher.id, self.teacher.id)
        self.assertEqual(new_class.title, 'Advanced English')

    def test_view_english_class(self):
        class_id = self.english_class.pk
        self.client.login(username='teacher', password='teacherpass')
        response = self.client.get(reverse('update_english_class', kwargs={'pk': class_id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.english_class.title)

    def test_create_lesson_by_teacher(self):
        self.client.login(username='teacher', password='teacherpass')
        english_class = EnglishClass.objects.create(title="Test Class", teacher=self.teacher)
        lessons_count_before = Lesson.objects.count()
        response = self.client.post(reverse('create_lesson', kwargs={'class_id': english_class.pk}), data={
            'title': 'Test Lesson',
            'description': 'Test Description',
            'start_time': '2023-01-01T10:00:00Z',
            'end_time': '2023-01-01T12:00:00Z',
            'location': 'on-site',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Lesson.objects.count(), lessons_count_before + 1)
        new_lesson = Lesson.objects.latest('id')
        self.assertEqual(new_lesson.title, 'Test Lesson')
        self.assertEqual(new_lesson.english_class, english_class)
