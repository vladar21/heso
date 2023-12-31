# HESO: Home English School Online

## Introduction
HESO is an innovative online platform tailored for small-scale English language schools, integrating class management, personalized scheduling, file sharing, AI chatbot assistance, and Google Meet integration. It features distinct user roles and functionalities for an effective online learning environment.

## Table of Contents
- [Overview](#overview)
- [User Roles and Responsibilities](#user-roles-and-responsibilities)
- [Classes Description](#classes-description)
- [Google Meet and Calendar API Integration](#google-meet-and-calendar-api-integration)
- [AI Chatbot Integration](#ai-chatbot-integration)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview
HESO is designed to streamline the educational process in online English language schools, offering comprehensive tools for managing classes, facilitating interactive learning, and ensuring efficient communication.

## User Roles and Responsibilities
### SuperAdmin
- Oversees the entire platform, managing global settings and user accounts.
- Monitors platform activities and generates reports.

### Teacher
- Manages English classes, schedules, and educational materials.
- Interacts with students and provides feedback.

### Student
- Enrolls in classes, accesses schedules and materials.
- Participates in classes and interacts with teachers.

## Classes Description
### User (Abstract Base Class)
- Represents a generic user in the system.
- Attributes: User ID, Name, Email, Password.
- Methods: Login, Logout, UpdateProfile.
- Relationships: Base class for SuperAdmin, Teacher, and Student.

### SuperAdmin (Subclass of User)
- Inherits from User.
- Additional Responsibilities: Manages platform settings, oversees all platform activities, generates reports.

### Teacher (Subclass of User)
- Inherits from User.
- Additional Responsibilities: Manages English classes, schedules, and educational materials, interacts with students.
- Relationships: Associated with EnglishClasses and Schedules.

### Student (Subclass of User)
- Inherits from User.
- Additional Responsibilities: Enrolls in classes, accesses schedules and materials, participates in classes.
- Relationships: Enrolled in EnglishClasses.

### EnglishClass
- Represents a course with content and schedule.
- Attributes: Class ID, Title, Description, Teacher ID, Schedule ID, Student List, Material List, Lesson List.
- Relationships: Contains Materials and Lessons; associated with a specific Teacher and enrolled Students.

### Schedule
- Organizes the timetable for EnglishClasses and their respective Lessons.
- Attributes: Schedule ID, EnglishClass ID, List of Lesson IDs.
- Relationships: Associated with EnglishClass and Teacher; comprises Lessons.

### Lesson
- Represents individual class sessions within an EnglishClass.
- Attributes: Lesson ID, EnglishClass ID, Date, Time, Google Meet Link, Attendance Record.
- Relationships: Part of a Schedule; organized and managed by the Teacher; linked to specific Materials.

### Material
- Educational content for classes.
- Attributes: Material ID, Title, Type (Video, Document, etc.), Access Level.
- Relationships: Can be associated with multiple EnglishClasses and Lessons as required. This association is managed externally, allowing for flexible use across the platform.

### GoogleCalendarEvent
- Represents a calendar event created for a lesson.
- Attributes: Event ID, Lesson ID, Start Time, End Time, Google Meet Link.
- Relationships: Corresponds to a specific Lesson; used to store and retrieve meeting details.

### AI Chatbot
- Provides automated support and assistance.
- Attributes: Chatbot ID, User Query History.
- Relationships: Interacts with Teachers and Students.

## Google Meet Integration via Google Calendar API
### Creating Meetings with Google Calendar API
- **Automated Event Creation**: Utilizes Google Calendar API to create calendar events when a lesson is scheduled in HESO.
- **Meet Link Generation**: Google Calendar automatically generates a Google Meet link for each event.
- **Meet Link Retrieval**: The API returns event details, including the Meet link, which is then stored in HESO.

### Storing and Accessing Meet Links
- **Link Storage**: Store the Google Meet link in HESO, associated with the corresponding lesson.
- **Link Accessibility**: Teachers and students can access the Meet links via their HESO schedules.

### Security and Access Control
- **Enrollment-based Access**: Only enrolled students and assigned teachers can access the Meet links.
- **Authentication System**: Managed within HESO's user authentication and authorization system.

### Free Usage and Implementation
- **Google Cloud's Free Tier**: The Google Calendar API is part of Google Cloud's free tier, usually including a generous usage quota.
- **API Credentials**: Create OAuth 2.0 Client ID in Google Cloud Console for application authentication.

### Steps for Integration
1. **Set Up Google Cloud Project**: Create a project and enable Google Calendar API.
2. **Backend Implementation**: Integrate the API logic in the Python/Django backend.
3. **Frontend UI Updates**: Update the frontend to display the Meet links.
4. **Testing and Deployment**: Ensure reliable operation of the integration, particularly the generation and accessibility of Meet links.

### Important Considerations
- **API Quota**: Monitor the usage to stay within Google's free tier limits.
- **User Data Security**: Ensure compliance with privacy regulations.
- **User Permissions**: Users must grant HESO permission to manage their calendars.


## AI Chatbot Integration
- AI-driven support for scheduling and learning.
- Personalized interaction for user experience enhancement.

## Technologies Used
- **Backend**: Python, Django
- **Frontend**: Bootstrap 4, jQuery
- **AI Chatbot**: ChatterBot
- **Database**: SQLite (development), PostgreSQL (production)
- **Version Control**: Git, GitHub

## Setup and Installation
- Instructions for setting up the environment and installing dependencies.

## Usage
- Guidance for SuperAdmins, Teachers, and Students on platform interaction.

## Testing
- Strategies for automated and manual testing of the platform.

## Contributing
- Guidelines for contributing to the HESO project.

## License
- Details about the project's licensing terms.

## Acknowledgments
- Special thanks to all the contributors, testers, and supporters of HESO.
