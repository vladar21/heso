# Standard library imports
import json
from zoneinfo import ZoneInfo

# Third-party imports (Django is considered a third-party library)
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_POST


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
        teachers = Teacher.objects.filter(taught_classes__lessons=lesson)
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
    # Handle POST request to update lesson details
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        lesson_id = data.get('id')
        start_time = data.get('start')
        end_time = data.get('end')
        
        # Convert time strings to datetime objects considering the timezone
        start_time = parse_datetime(start_time).replace(tzinfo=ZoneInfo("Europe/Dublin")) if start_time else None
        end_time = parse_datetime(end_time).replace(tzinfo=ZoneInfo("Europe/Dublin")) if end_time else None
        
        # Update the lesson in the database
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
            lesson.start_time = start_time if start_time else lesson.start_time
            lesson.end_time = end_time if end_time else lesson.end_time
            lesson.save()
            return JsonResponse({'status': 'success', 'message': 'Lesson updated successfully.'})
        except Lesson.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Lesson not found.', 'lesson_id': lesson_id}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
