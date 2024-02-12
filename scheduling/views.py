from django.shortcuts import render
# from django.http import HttpResponse
from .models import Lesson


def schedule(request):
    lessons = Lesson.objects.all()
    lessons_list = [
        {
            'id': lesson.id,
            'title': lesson.title,
            'start': lesson.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': lesson.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'url': f"/lessons/{lesson.id}/",
        } for lesson in lessons
    ]
    return render(request, 'scheduling/schedule.html', {'lessons_list': lessons_list})
