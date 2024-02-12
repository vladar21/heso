from django.shortcuts import render
import json
from .models import Lesson


def schedule(request):
    lessons = Lesson.objects.prefetch_related('english_class', 'english_class__teacher', 'english_class__students').all()
    lessons_data = []

    for lesson in lessons:
        total_lessons = lesson.english_class.lessons.count()
        lesson_number = list(lesson.english_class.lessons.order_by('start_time')).index(lesson) + 1

        lessons_data.append({
            'id': lesson.id,
            'title': f"{lesson.title} ({lesson_number}/{total_lessons})",
            'start': lesson.start_time.isoformat(),
            'end': lesson.end_time.isoformat(),
            'color': lesson.english_class.color,
            'backgroundColor': lesson.english_class.color,
            'extendedProps': {
                'teacher': lesson.english_class.teacher.username,
                'students': list(lesson.english_class.students.values_list('username', flat=True)),
                'classTitle': lesson.english_class.title
            }
        })

    return render(request, 'scheduling/schedule.html', {'lessons_list': json.dumps(lessons_data)})
