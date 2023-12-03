# HESO: Home English School Online

## Introduction
HESO is an innovative online platform tailored for small-scale English language schools. It integrates class management, personalized scheduling, file sharing, AI chatbot assistance, and Google Meet integration, all structured around distinct user roles for an effective and interactive online learning environment.

## Table of Contents
- [Overview](#overview)
- [User Roles and Responsibilities](#user-roles-and-responsibilities)
- [Key Objects and Functionalities](#key-objects-and-functionalities)
- [Google Meet Integration](#google-meet-integration)
- [AI Chatbot Integration](#ai-chatbot-integration)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview
HESO is designed to streamline the educational process in online English language schools, offering a comprehensive suite of tools for managing classes, facilitating interactive learning, and ensuring efficient communication.

## User Roles and Responsibilities
### SuperAdmin
- Oversees the entire platform, managing global settings and user accounts.
- Monitors platform activities and generates reports.

### Teacher
- Creates, updates, and manages English classes.
- Links classes with personalized schedules and manages educational materials.
- Interacts with students for class activities and manages enrollments.

### Student
- Enrolls in classes and accesses personalized schedules.
- Utilizes educational materials and participates in class activities.
- Engages with AI chatbot for learning support and schedule management.

## Key Objects and Functionalities
### EnglishClass
- Central to course delivery, associated with specific teachers, students, schedules, and materials.

### Schedule
- Manages the timetable for all classes, integrating personalized schedules for teachers and students.
- Comprises all Lessons, facilitating automatic scheduling and updates.

### Lesson
- Represents individual class sessions.
- Integrates with Google Meet for online lessons, handling invitations and attendance tracking.

## Google Meet Integration
- Seamless generation of Google Meet links for each scheduled lesson.
- Embedding Meet links into class schedules for easy access by teachers and students.
- Ensuring secure access to online lessons for registered class participants.

## AI Chatbot Integration
- Provides personalized assistance for scheduling and learning.
- Offers educational tips and language translation services.
- Enhances user interaction and engagement with the learning material.

## Technologies Used
- **Backend**: Python with Django
- **Frontend**: Bootstrap 4 and jQuery
- **AI Chatbot**: Powered by ChatterBot
- **Database**: SQLite for development and PostgreSQL for production
- **Version Control**: Git and GitHub

## Setup and Installation
- Detailed steps for setting up the development environment and installing dependencies.

## Usage
- Instructions for SuperAdmins, Teachers, and Students on interacting with and utilizing the platform's features.

## Testing
- Overview of strategies for both automated and manual testing, ensuring functionality and smooth integration.

## Contributing
- Guidelines for contributing to the HESO project, including coding standards and submission processes.

## License
- Information regarding the project's licensing terms.

## Acknowledgments
- Special thanks to all the contributors, testers, and supporters who have helped in developing HESO.
