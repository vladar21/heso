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

## Google Meet and Calendar API Integration
### Google Meet Integration
- Automated Google Meet link generation for lessons.
- Calendar synchronization to include Meet links in lesson schedules.
- Secured access to ensure only enrolled students and designated teachers can join.

### Implementing Google Calendar API
- **Creating Meetings with Google Calendar API**: Utilizes the API to create calendar events when a lesson is scheduled, automatically generating a Google Meet link.
- **Storing and Accessing Meet Links**: Meet links are stored and made accessible within HESO, linked to corresponding lessons.
- **Security and Access Control**: Ensures that Meet links are accessible only to enrolled students and assigned teachers.

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
