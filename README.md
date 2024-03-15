# HESO: Home English School Online – Online Class Schedule Service

[View the live project - Click here.](https://heso-cba8b8a64704.herokuapp.com/)

## Introduction
HESO is a streamlined online service designed for managing class schedules in small-scale English language schools. It features an admin section where students and teachers can interact with the class schedule.

## Table of Contents
- [Overview](#overview)
- [User Roles and Responsibilities](#user-roles-and-responsibilities)
- [User Stories](#user-stories)
- [Model Relationships](#model-relationships)
- [System Features](#system-features)
- [Google Calendar API Integration](#google-calendar-api-integration)
- [Technologies Used](#technologies-used)
- [Agile Development Plan](#agile-development-plan)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview
HESO is tailored to facilitate the organization and management of class schedules, enhancing the efficiency of educational processes in online English language schools.

## User Roles and Responsibilities

### SuperAdmin
- Manages user accounts and overall system settings.
- Oversees scheduling operations and system maintenance.

### Teacher
- Accesses and interacts with the class schedule.
- Coordinates with students regarding class timings.

### Student
- Views class schedules.

## User Stories

In the development of HESO, user stories are used to capture specific functionalities from the perspective of different users. These stories help in guiding the development process under Agile methodology.

### User Story for Admin
- **Story**: As an **Admin**, I can **manage user accounts and system settings** so that **the system remains secure and functions as intended**.
  - **Acceptance Criteria**:
    1. Admin can create, edit, and delete user accounts for teachers and students.
    2. Admin can access and modify system settings including platform features and access controls.
    3. Admin can CRUD class schedules and lesson plans to ensure accuracy and coherence.
    4. Admin can CRUD educational materials uploaded by teachers to maintain quality standards.

### User Story for Teacher
- **Story**: As a **Teacher**, I can **access and update the class schedule** so that **I can efficiently manage class timings and inform students of any changes**.
  - **Acceptance Criteria**:
    1. Teacher can CRUD their class schedules.
    2. Any changes made are automatically updated and visible to students.

### User Story for Student
- **Story**: As a **Student**, I can **view my class schedule** so that **I can keep track of class timings and any updates to the schedule**.
  - **Acceptance Criteria**:
    1. Student can access classes schedule.
    2. Schedule updates are immediately visible to the student.

### User Story for Integration with Google Calendar (feature )
- **Story**: As a **User (Teacher/Student)**, I can **have the class schedule synchronized with Google Calendar** so that **I can receive reminders and view my schedule in a familiar interface**.
  - **Acceptance Criteria**:
    1. Class schedules are automatically synced with Google Calendar.
    2. Users receive notifications for upcoming classes through Google Calendar.
    3. Users can view class details within their Google Calendar interface.

## Model Relationships

### User Model (Abstract Base Class)
```plaintext
- id (PrimaryKey): Unique identifier for the user.
- username (CharField): Chosen username for login purposes.
- email (EmailField): Email address for communication and system notifications.
- phone_number (CharField): Phone number for communication.
- first_name (CharField): User's given name for identification within the system.
- last_name (CharField): User's family name for record-keeping.
- password (CharField): Hashed password for secure authentication.
- is_teacher (BooleanField): Flag to indicate if the user has teacher privileges.
- is_student (BooleanField): Flag to indicate if the user has student privileges.
```

### Admin Model (Inherits from User)
```plaintext
- Inherits all fields from User.
- Additional Privileges: Full access to the platform for managing settings, users, and system-wide configurations.
```

### Teacher Model (Inherits from User)
```plaintext
- department (CharField): The department to which the teacher belongs.
- bio (TextField, optional): A brief description of the teacher's background and teaching philosophy.
```

### Student Model (Inherits from User)
```plaintext
- enrollment_date (DateTimeField): The date on which the student was enrolled in the school.
- major (CharField, optional): The main subject or discipline the student is studying.
```

### EnglishClass Model
```plaintext
- id (PrimaryKey): Unique identifier for the class.
- title (CharField): The formal name of the class or course.
- description (TextField): Detailed curriculum and information about the class.
- teacher (ForeignKey to Teacher): The teacher who conducts the class.
- schedule (ForeignKey to Schedule): The schedule associated with the class.
- students (ManyToManyField to Student): The list of students enrolled in the class.
```

### Schedule Model
```plaintext
- id (PrimaryKey): Unique identifier for the schedule.
- class_id (ForeignKey to EnglishClass): The class to which this schedule belongs.
- term (CharField): The academic term or semester during which the class is held.
- start_date (DateField): The starting date of the class's schedule.
- end_date (DateField): The ending date of the class's schedule.
```

### Lesson Model
```plaintext
- id (PrimaryKey): Unique identifier for the lesson.
- schedule (ForeignKey to Schedule): The schedule to which this lesson belongs.
- title (CharField): The title or topic of the individual lesson.
- description (TextField, optional): Additional details about the lesson's content.
- start_time (DateTimeField): The scheduled start time of the lesson.
- end_time (DateTimeField): The scheduled end time of the lesson.
- google_meet_link (URLField, optional): The URL for the Google Meet session, if applicable.
```

### Material Model
```plaintext
- id (PrimaryKey): Unique identifier for the material.
- title (CharField): The title or name of the material.
- type (CharField): The type of material, such as Video, Document, etc.
- content (TextField/FileField): The actual educational content, which may be a file upload or plain text.
- english_classes (ManyToManyField to EnglishClass): A collection of classes that this material is associated with.
- lessons (ManyToManyField to Lesson): A collection of lessons that use this material.
- students (ManyToManyField to Student): A collection of students who have access to this material.
- created_at (DateTimeField): The date and time when the material was created.
- updated_at (DateTimeField): The date and time when the material was last updated.
```

### GoogleCalendarEvent Model
```plaintext
- id (PrimaryKey): Unique identifier for the calendar event.
- lesson_id (ForeignKey to Lesson): The lesson associated with the calendar event.
- event_time (DateTimeField): The scheduled time of the event.
- google_event_id (CharField): The unique identifier for the event in Google Calendar.
```

## System Features
- **Class Schedule Management**: Teachers and students can view and interact with class schedules.
- **Admin Control**: System administrators can manage user accounts and configure system settings.


## Future Enhancements

- Google Calendar API Integration:

  **Automated Scheduling**: Class schedules are automatically synchronized with Google Calendar, offering a seamless integration for managing class timings.

  **Real-time Updates**: Teachers and students receive real-time updates and notifications through Google Calendar.

## Technologies Used
- **Backend**: Django 4.2.9
- **Frontend**: Bootstrap 4.6.2, jQuery 3.5.1, FullCalendar 6.1.10
- **Database**: PostgreSQL 13.9
- **Version Control**: Git, GitHub
- **Deployment**: Heroku

## Agile Development Plan

The development of HESO is structured into sprints, with each sprint targeting specific tasks for a focused and incremental development approach. Below is the sprint schedule along with their respective tasks:

### Sprint Schedule

#### Sprint 1 (28/01/2024 - 31/01/2024): Project Setup and Basic Backend
- Task 1: Set up the Django project and configure the development environment.
- Task 2: Establish database models for User, Teacher, Student, and Admin.
- Task 3: Implement a basic user authentication system.

#### Sprint 2 (01/02/2024 - 04/02/2024): Basic Frontend and User Management
- Task 4: Set up the basic structure of the frontend using Bootstrap and jQuery.
- Task 5: Implement frontend interfaces for user registration and login.
- Task 6: Develop Admin functionalities for managing user accounts.

#### Sprint 3 (05/02/2024 - 08/02/2024): Advanced Backend for Class and Schedule Management
- Task 7: Develop models and backend functionalities for EnglishClass and Schedule.
- Task 8: Implement Admin tools for class schedules and lesson plan management.

#### Sprint 4 (09/02/2024 - 12/02/2024): Frontend for Class and Schedule Management
- Task 9: Create frontend interfaces for class schedule viewing and editing.
- Task 10: Enable Teachers to modify class schedules through the frontend.

#### Sprint 5 (13/02/2024 - 16/02/2024): Lesson and Material Management
- Task 11: Develop models and backend functionalities for Lesson and Material.
- Task 12: Build Admin review and approval system for educational materials.

#### Sprint 6 (17/02/2024 - 20/02/2024): Google Calendar API Integration
- Task 13: Integrate backend with Google Calendar API for class schedule synchronization.
- Task 14: Set up syncing of class schedules with Google Calendar.

#### Sprint 7 (21/02/2024 - 24/02/2024): Frontend Integration and Notification System
- Task 15: Develop frontend integration for Google Calendar features.
- Task 16: Implement a notification system for schedule changes and upcoming classes.

#### Sprint 8 (25/02/2024 - 28/02/2024): Testing and Refinement
- Task 17: Conduct thorough unit and integration tests.
- Task 18: Refine user interfaces and functionalities based on feedback.

#### Sprint 9 (29/02/2024 - 03/03/2024): Documentation and Final Testing
- Task 19: Document the API and user interfaces.
- Task 20: Conduct user acceptance testing and finalize bug fixes.

#### Sprint 10 (04/03/2024 - 07/03/2024): Deployment and Launch
- Task 21: Set up the PostgreSQL production database.
- Task 22: Configure continuous integration and deployment pipelines.
- Task 23: Deploy the project on a hosting platform like Heroku.

Each sprint in this schedule is a focused development cycle that addresses specific components of the project, facilitating clear progression towards the project goals.

## Setup and Installation
- Detailed instructions for setting up the development environment and deploying the application.

## Usage
- Guidelines on how administrators, teachers, and students interact with the system.

## Testing

### Send emails

- For test sending mails feature in project using mailtrap.io service. Please, use credentials below to look ones:
 ```bash
 mailtrap link: https://mailtrap.io/inboxes/2689731/messages/4092718424
 mailtrap login: vlad.rastvorov@aol.com
 mailtrap password: :8xt:XP4fWr.mwe
 ```

### Unit tests for Users App

#### User Registration Form Test
- `test_form_valid`: Test that the user registration form is valid with correct data.
- `test_form_invalid`: Test that the user registration form is invalid with incorrect data.

#### User Registration Test
- `test_registration_page_status_code`: Test that the registration page returns a status code of 200.
- `test_registration_form`: Test that user registration is successful and an email is sent upon registration.

#### Logout Test
- `test_logout_redirect`: Test that logout redirects to the login page.

#### Login Test
- `test_login_page_status_code`: Test that the login page returns a status code of 200.
- `test_login_form_valid`: Test that login with valid credentials redirects to the expected page.

### Unit tests for Scheduling App

#### Schedule View Tests
- `test_schedule_view_for_anonymous_user`: Test that the schedule view is accessible to anonymous users.
- `test_schedule_view_for_student`: Test that the schedule view is accessible to students.
- `test_english_class_creation_by_teacher`: Test that teachers can create English classes.
- `test_english_class_creation_by_student`: Test that students are redirected when trying to create English classes.
- `test_update_english_class_by_teacher`: Test that teachers can update English classes.
- `test_delete_english_class_by_super_user`: Test that superusers can delete English classes.
- `test_lesson_details_access_by_teacher`: Test that teachers can access lesson details.
- `test_lesson_details_access_by_student`: Test that students can access lesson details.
- `test_lesson_details_access_by_anonymous_user`: Test that anonymous users cannot access lesson details.


## Bugs

### 1. Doubling while saving new material

- **Description:** When we add new material in the upload form, in the list of lesson materials we see double titles of ones.

  <img src="assets/images/doubling_while_saving_new_material.jpg" width="600" alt="doubling while saving new material">

- **Solution:** Using the get_or_create method on the backend, which allows you to get an existing material or create a new one if it doesn't exist.

  ```bash
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
  ```
  ### 2. Don't highlight current menu item

- **Description:** When the user clicks on a menu item that doesn't have an active class (highlighted in bold white).

  <img src="assets/images/not_highlighting_current_menu_item.jpg" width="600" alt="not highlighting current menu item">

- **Solution:** Need accurate writing of the URL to use for comparisons.

 <img src="assets/images/fix_not_highlighting_current_menu_item.jpg" width="600" alt="fix not highlighting current menu item">

## Contributing
- Information for developers interested in contributing to the HESO project.

## License
- Details about the licensing terms for the project.

## Acknowledgments
- A thank you to all the contributors, testers, and supporters who have helped in the development of HESO.
