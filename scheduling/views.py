# scheduling/views.py

# Standard library imports
import json

# Third-party imports (Django is considered a third-party library)
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods


# Local application imports
from .models import Lesson, Material
# from users.models import Teacher, Student
from users.models import User
from .forms import EnglishClassForm, ScheduleForm
from .models import EnglishClass, Schedule


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def schedule(request):
    # Fetch all lessons with related class, teacher, and students data
    lessons = Lesson.objects.prefetch_related('english_class', 'english_class__teacher', 'english_class__students').all()
    lessons_data = []
    teachers = list(User.objects.filter(is_teacher=True).values('id', 'username'))
    is_readonly = request.user.is_student

    # Prepare lessons data for FullCalendar
    for lesson in lessons:
        total_lessons = lesson.english_class.lessons.count()
        lesson_number = list(lesson.english_class.lessons.order_by('start_time')).index(lesson) + 1
        # teachers = Teacher.objects.filter(taught_classes__lessons=lesson)
        teacher_id = lesson.english_class.teacher.id if lesson.english_class.teacher else None
        student_usernames_ids = list(lesson.english_class.students.values('id', 'username'))
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
                'teacher_id': teacher_id,
                'teachers': teachers,
                'students': student_usernames_ids,
                'materials': list(materials.values('id', 'title')),
            }
        })

    # Render the schedule page with lessons data
    return render(request, 'scheduling/schedule.html', {'lessons_list': json.dumps(lessons_data), 'is_readonly': is_readonly})


@csrf_exempt
@require_POST
def lesson_details(request):
    data = json.loads(request.body)
    lesson_id = data.get('lessonId')
    
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access. Please log in.'}, status=403)
    
    lesson = get_object_or_404(Lesson, pk=lesson_id)

    if not (request.user.is_superuser or request.user == lesson.english_class.teacher or request.user in lesson.english_class.students.all()):
        return JsonResponse({'status': 'error', 'message': 'You do not have permission to view this lesson.'}, status=403)
    
    total_lessons = lesson.english_class.lessons.count()
    lesson_number = list(lesson.english_class.lessons.order_by('start_time')).index(lesson) + 1
    
    teachers = User.objects.filter(is_teacher=True)
    students = lesson.english_class.students.all()
    materials = lesson.materials.all()

    lesson_data = {
        'id': lesson.id,
        'title': f"{lesson.english_class.title} ({lesson_number}/{total_lessons}) | {lesson.english_class.teacher.username if lesson.english_class.teacher else 'No teacher'}",
        'start': lesson.start_time.isoformat(),
        'end': lesson.end_time.isoformat(),
        'backgroundColor': lesson.english_class.color,
        'extendedProps': {
            'class_topic': lesson.title,
            'description': lesson.description,
            'meeting_link': lesson.meeting_link if lesson.location == 'online' else '',
            'location': lesson.location,
            'teacher_id': lesson.english_class.teacher.id if lesson.english_class.teacher else None,
            'teachers': [{'id': teacher.id, 'username': teacher.username} for teacher in teachers],
            'students': [{'id': student.id, 'username': student.username} for student in students],
            'materials': [{'id': material.id, 'title': material.title} for material in materials],
        }
    }

    return JsonResponse({'status': 'success', 'lesson': lesson_data}, status=200)


@csrf_exempt
@require_POST
def update_lesson(request):
    if not request.user.is_authenticated and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    
    if request.content_type == 'application/json':
        data = json.loads(request.body.decode('utf-8'))
        lesson_id = data.get('id')
    else:
        data = request.POST
        lesson_id = data['lessonId']

    try:
        lesson = Lesson.objects.select_related('english_class').get(pk=lesson_id)

        if not (request.user.is_superuser or request.user == lesson.english_class.teacher):
            return JsonResponse({'status': 'error', 'message': 'You do not have permission to update this lesson.'}, status=403)
        
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
                teacher_id = data['teacher']
                try:
                    teacher = User.objects.filter(pk=teacher_id, is_teacher=True).first()
                    lesson.english_class.teacher = teacher
                    lesson.english_class.save()
                    total_lessons = lesson.english_class.lessons.count()
                    lesson_number = list(lesson.english_class.lessons.order_by('start_time')).index(lesson) + 1
                    lesson.title = f"{lesson.english_class.title} ({lesson_number}/{total_lessons}) | {teacher.username}"
                except User.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Teacher not found.'}, status=404)

            # Update students if provided
            if 'students' in data:
                student_ids = data['students']
                students = User.objects.filter(id__in=student_ids, is_student=True)
                lesson.english_class.students.set(students)

            # Update materials if provided
            if 'materials' in data:
                material_ids = data['materials']
                lesson.materials.clear()
                lesson.materials.set(Material.objects.filter(id__in=material_ids))
            
            if request.FILES.getlist('new_materials'):
                for uploaded_file in request.FILES.getlist('new_materials'):
                    if uploaded_file:
                        material, created = Material.objects.get_or_create(
                            title=uploaded_file.name,
                            type="file",
                            content=uploaded_file.read()
                        )
                        if created:
                            lesson.materials.add(material)
            
            lesson.save()

            updated_lesson = Lesson.objects.get(pk=lesson_id)

            total_lessons = updated_lesson.english_class.lessons.count()
            lesson_number = list(updated_lesson.english_class.lessons.order_by('start_time')).index(updated_lesson) + 1
            teachers = User.objects.filter(is_teacher=True)
            students = User.objects.filter(is_student=True, enrolled_classes__lessons=updated_lesson)
            materials = Material.objects.filter(lessons=updated_lesson)

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


@login_required
def create_english_class(request):
    if not (request.user.is_superuser or request.user.is_teacher):
        messages.error(request, "You do not have permission to create a class.")
        return redirect('english_class_list')
    
    if request.method == 'POST':
        class_form = EnglishClassForm(request.POST)
        schedule_form = ScheduleForm(request.POST)
        if class_form.is_valid() and schedule_form.is_valid():
            new_class = class_form.save()
            new_schedule = schedule_form.save(commit=False)
            new_schedule.english_class = new_class
            new_schedule.save()
            messages.success(request, "Class created successfully.")
            return redirect('english_class_list')
    else:
        class_form = EnglishClassForm()
        schedule_form = ScheduleForm()
    
    context = {
        'class_form': class_form,
        'schedule_form': schedule_form,
    }
    return render(request, 'scheduling/create_english_class.html', context)


@login_required
def update_english_class(request, pk):
    english_class = get_object_or_404(EnglishClass, pk=pk)
    schedule, created = Schedule.objects.get_or_create(english_class=english_class)

    if not (request.user.is_superuser or request.user == english_class.teacher):
        messages.error(request, "You do not have permission to update this class.")
        return redirect('english_class_list')
    
    if request.method == 'POST':
        class_form = EnglishClassForm(request.POST, instance=english_class)
        schedule_form = ScheduleForm(request.POST, instance=schedule)
        
        if class_form.is_valid() and schedule_form.is_valid():
            class_form.save()
            schedule_form.save()

            messages.success(request, "Class updated successfully.")
            
            return redirect('english_class_list')
    else:
        class_form = EnglishClassForm(instance=english_class)
        schedule_form = ScheduleForm(instance=schedule)
    
    context = {
        'class_form': class_form,
        'schedule_form': schedule_form,
        'english_class': english_class  
    }

    return render(request, 'scheduling/update_english_class.html', context)


@login_required
def english_class_list(request):
    if request.user.is_superuser or request.user.is_teacher:
        if request.user.is_superuser:
            schedules = Schedule.objects.all()
        else:
            schedules = Schedule.objects.filter(english_class__teacher=request.user)
        return render(request, 'scheduling/english_class_list.html', {'schedules': schedules})
    else:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('schedule')


@login_required
def delete_english_class(request, pk):
    schedule = get_object_or_404(Schedule, english_class__pk=pk)

    if not (request.user.is_superuser or request.user == schedule.teacher):
        messages.error(request, "You do not have permission to delete this class.")
        return redirect('english_class_list')
    
    if request.method == 'POST':
        schedule.delete()

        messages.success(request, "Class deleted successfully.")

        return redirect('english_class_list')
    
    return render(request, 'scheduling/delete_english_class.html', {'english_class': schedule.english_class})
