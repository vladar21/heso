# Standard library imports
import json
from zoneinfo import ZoneInfo

# Third-party imports (Django is considered a third-party library)
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db import transaction


# Local application imports
from .models import Lesson, Material
from users.models import Teacher, Student


def schedule(request):
    # Fetch all lessons with related class, teacher, and students data
    lessons = Lesson.objects.prefetch_related('english_class', 'english_class__teacher', 'english_class__students').all()
    lessons_data = []

    # Prepare lessons data for FullCalendar
    for lesson in lessons:
        total_lessons = lesson.english_class.lessons.count()
        lesson_number = list(lesson.english_class.lessons.order_by('start_time')).index(lesson) + 1
        # teachers = Teacher.objects.filter(taught_classes__lessons=lesson)
        teachers = Teacher.objects.all()
        students = Student.objects.filter(enrolled_classes__lessons=lesson)
        materials = Material.objects.filter(lessons=lesson)

        lessons_data.append({
            'id': lesson.id,
            'title': f"{lesson.english_class.title} ({lesson_number}/{total_lessons}) | {lesson.english_class.teacher.username}",
            'start': lesson.start_time.isoformat(),
            'end': lesson.end_time.isoformat(),
            'backgroundColor': lesson.english_class.color,
            'extendedProps': {
                'class_topic': lesson.title,
                'description': lesson.description,
                'meeting_link': lesson.meeting_link,
                'location': lesson.location,
                'teacher_id': lesson.english_class.teacher.id,
                'teachers': list(teachers.values('id', 'username')),
                'students': list(students.values('id', 'username')),
                'materials': list(materials.values('id', 'title')),
            }
        })

    # Render the schedule page with lessons data
    return render(request, 'scheduling/schedule.html', {'lessons_list': json.dumps(lessons_data)})


@csrf_exempt
@require_POST
def update_lesson(request):
    if request.content_type == 'application/json':
        data = json.loads(request.body.decode('utf-8'))
        lesson_id = data.get('id')
    else:
        data = request.POST
        lesson_id = data['lessonId']

    print(data)  # Выводим полученные данные для проверки

    try:
        lesson = Lesson.objects.select_related('english_class').get(pk=lesson_id)
        
        with transaction.atomic():
            # Update lesson fields if they are provided
            if 'description' in data:
                lesson.description = data['description']
            if 'start' in data:
                lesson.start_time = parse_datetime(data['start']).astimezone(timezone.get_default_timezone())
            if 'end' in data:
                lesson.end_time = parse_datetime(data['end']).astimezone(timezone.get_default_timezone())
            if 'location' in data:
                lesson.location = data['location']
            if 'meeting_link' in data and lesson.location == 'online':
                lesson.meeting_link = data['meeting_link']
            else:
                lesson.meeting_link = None  # Clear meeting link if location is not online

            # Update the teacher if provided
            if 'teacher' in data:
                try:
                    teacher = Teacher.objects.get(pk=data['teacher'])
                    lesson.english_class.teacher = teacher
                    lesson.english_class.save()
                    total_lessons = lesson.english_class.lessons.count()
                    lesson_number = list(lesson.english_class.lessons.order_by('start_time')).index(lesson) + 1
                    lesson.title = f"{lesson.english_class.title} ({lesson_number}/{total_lessons}) | {teacher.username}"
                except Teacher.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Teacher not found.'}, status=404)

            # Update students if provided
            if 'students' in data:
                student_ids = data['students']
                lesson.english_class.students.set(Student.objects.filter(id__in=student_ids))

            # Update materials if provided
            if 'materials' in data:
                material_ids = data['materials']
                lesson.materials.set(Material.objects.filter(id__in=material_ids))
            
            lesson.save()

            # Проверяем, действительно ли данные урока изменились в базе данных
            updated_lesson = Lesson.objects.get(pk=lesson_id)

            # Подготавливаем данные обновленного урока для передачи в шаблон
            total_lessons = updated_lesson.english_class.lessons.count()
            lesson_number = list(updated_lesson.english_class.lessons.order_by('start_time')).index(updated_lesson) + 1
            teachers = Teacher.objects.all()
            students = Student.objects.filter(enrolled_classes__lessons=updated_lesson)
            materials = Material.objects.filter(lessons=updated_lesson)

            # Формируем словарь с обновленными данными урока
            updated_lesson_data = {
                'id': updated_lesson.id,
                'title': f"{updated_lesson.english_class.title} ({lesson_number}/{total_lessons}) | {updated_lesson.english_class.teacher.username}",
                'start': updated_lesson.start_time.isoformat(),
                'end': updated_lesson.end_time.isoformat(),
                'backgroundColor': updated_lesson.english_class.color,
                'extendedProps': {
                    'class_topic': updated_lesson.title,
                    'description': updated_lesson.description,
                    'meeting_link': updated_lesson.meeting_link,
                    'location': updated_lesson.location,
                    'teacher_id': updated_lesson.english_class.teacher.id,
                    'teachers': list(teachers.values('id', 'username')),
                    'students': list(students.values('id', 'username')),
                    'materials': list(materials.values('id', 'title')),
                }
            }

            print("lesson :", updated_lesson_data)

            return JsonResponse({'status': 'success', 'message': 'Lesson updated successfully.', 'lesson': updated_lesson_data})
    except Lesson.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Lesson not found.'}, status=404)
    except ObjectDoesNotExist:
        # This captures both Student.DoesNotExist and Material.DoesNotExist
        return JsonResponse({'status': 'error', 'message': 'One or more related objects not found.'}, status=404)
    except Exception as e:
        # General exception catch to handle unforeseen errors
        return JsonResponse({'status': 'error', 'message': f'Unexpected error: {str(e)}'}, status=400)
