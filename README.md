# HESO: Home English School Online – Online Class Schedule Service

## Introduction
HESO is a streamlined online service designed for managing class schedules in small-scale English language schools. It features an admin section where students and teachers can interact with the class schedule, integrated seamlessly with Google Calendar API.

## Table of Contents
- [Overview](#overview)
- [User Roles and Responsibilities](#user-roles-and-responsibilities)
- [User Stories](#user-stories)
- [System Features](#system-features)
- [Google Calendar API Integration](#google-calendar-api-integration)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview
HESO is tailored to facilitate the organization and management of class schedules, enhancing the efficiency of educational processes in online English language schools.

## User Roles and Responsibilities
### Admin
- Manages user accounts and overall system settings.
- Oversees scheduling operations and system maintenance.

### Teacher
- Accesses and interacts with the class schedule.
- Coordinates with students regarding class timings.

### Student
- Views class schedules.
- Receives updates and notifications on class timings.

## User Stories

In the development of HESO, user stories are used to capture specific functionalities from the perspective of different users. These stories help in guiding the development process under Agile methodology.

### User Story for Admin
- **Story**: As an **Admin**, I can **manage user accounts and system settings** so that **the system remains secure and functions as intended**.
  - **Acceptance Criteria**:
    1. Admin can create, edit, and delete user accounts.
    2. Admin can access and modify system settings.
    3. System security measures are in place to prevent unauthorized access.

### User Story for Teacher
- **Story**: As a **Teacher**, I can **access and update the class schedule** so that **I can efficiently manage class timings and inform students of any changes**.
  - **Acceptance Criteria**:
    1. Teacher can view their class schedules.
    2. Teacher can make modifications to the schedule.
    3. Any changes made are automatically updated and visible to students.

### User Story for Student
- **Story**: As a **Student**, I can **view my class schedule** so that **I can keep track of class timings and any updates to the schedule**.
  - **Acceptance Criteria**:
    1. Student can access their class schedule.
    2. Schedule updates are immediately visible to the student.
    3. Student receives notifications for any changes in the schedule.

### User Story for Integration with Google Calendar
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
- first_name (CharField): User's given name for identification within the system.
- last_name (CharField): User's family name for record-keeping.
- password (CharField): Hashed password for secure authentication.
- is_teacher (BooleanField): Flag to indicate if the user has teacher privileges.
- is_student (BooleanField): Flag to indicate if the user has student privileges.
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

## System Features
- **Class Schedule Management**: Teachers and students can view and interact with class schedules.
- **Admin Control**: System administrators can manage user accounts and configure system settings.

## Google Calendar API Integration
- **Automated Scheduling**: Class schedules are automatically synchronized with Google Calendar, offering a seamless integration for managing class timings.
- **Real-time Updates**: Teachers and students receive real-time updates and notifications through Google Calendar.

## Technologies Used
- **Backend**: Django 4.2.9
- **Frontend**: Bootstrap 4.6.1, jQuery 3.5.1
- **Database**: SQLite (development), PostgreSQL (production)
- **Version Control**: Git, GitHub

## Setup and Installation
- Detailed instructions for setting up the development environment and deploying the application.

## Usage
- Guidelines on how administrators, teachers, and students interact with the system.

## Testing
- Outline of testing strategies for ensuring system functionality and reliability.

## Contributing
- Information for developers interested in contributing to the HESO project.

## License
- Details about the licensing terms for the project.

## Acknowledgments
- A thank you to all the contributors, testers, and supporters who have helped in the development of HESO.
