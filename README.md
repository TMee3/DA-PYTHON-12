# 🚀 Epic Events CRM 🚀

Dive into the innovative Epic Events CRM, crafted for efficient management of clients, contracts, and events.


Epic Events CRM is a comprehensive, student-designed project from OpenClassrooms. This CRM system stands out for its command-line interface, prioritizing security and ease of use. It offers an advanced permission framework, Sentry logging for robust security, and a streamlined approach to managing clients, contracts, and events. Unique in its design, Epic Events CRM caters to businesses seeking a secure and efficient CRM solution.
***
## 📚 Contents
1. [🌟 Overview](#overview)
2. [💻 Tech Stack](#tech-stack)
3. [🔧 Setup Guide](#setup-guide)
4. [🔑 How to Use](#how-to-use)
5. [🧪 Testing](#testing)
6. [🛠️ Sentry Monitoring](#sentry-monitoring)

### 🌟 Overview

The Epic Events CRM leverages a variety of technologies, each playing a critical role:
- [Python](https://www.python.org/): The primary programming language, offering versatility and a wide range of libraries.
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/2.0.20/): ORM for database management, simplifying data operations.
- [Click](https://pypi.org/project/click/): For creating command-line interfaces, enhancing user interaction.
- [Python-dotenv](https://pypi.org/project/python-dotenv/): Manages environment variables, ensuring secure configuration.
- [Psychopg2-binary](https://pypi.org/project/psycopg2-binary/2.9.7/): PostgreSQL adapter, enabling robust database interactions.
- [Argon2-cffi](https://pypi.org/project/argon2-cffi/): For secure password hashing, ensuring user data protection.
***
Epic Events CRM is a student-designed project from OpenClassrooms, focusing on a secure, command-line based Customer Relationship Management system. It includes an advanced permission framework and Sentry logging for enhanced security and oversight.

### 💻 Tech Stack

Refer to the [Setup Guide](#setup-guide) for detailed instructions on getting started, including environment setup, dependencies installation, and initial configuration steps. The guide includes troubleshooting tips for common setup challenges.
*** 
- [Python](https://www.python.org/): Version ^3.10
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/2.0.20/): Version ^2.0.20
- [Click](https://pypi.org/project/click/): Version ^8.1.7
- [Python-dotenv](https://pypi.org/project/python-dotenv/): Version ^1.0.0
- [Psychopg2-binary](https://pypi.org/project/psycopg2-binary/2.9.7/): Version ^2.9.7
- [Argon2-cffi](https://pypi.org/project/argon2-cffi/): Version ^23.1.0
- [Pyjwt](https://pypi.org/project/PyJWT/): Version ^2.8.0
- [Pytest](https://pypi.org/project/pytest/7.4.2/): Version ^7.4.2
- [Flake8](https://pypi.org/project/flake8/): Version ^6.1.0
- [Coverage](https://pypi.org/project/coverage/): Version ^7.3.1
- [Pytest-sqlalchemy-mock](https://pypi.org/project/pytest-sqlalchemy-mock/): Version ^0.1.5
- [Sentry-sdk](https://pypi.org/project/sentry-sdk/1.35.0/): Version ^1.35.0
- [Poetry](https://pypi.org/project/poetry/1.6.1/): Version 1.6.1


### 🔧 Setup Guide

The [How to Use](#how-to-use) section provides comprehensive instructions on operating the CRM, complete with command-line examples, user scenarios, and visual aids like screenshots, making it accessible for users of all skill levels.
***
Prerequisites: Python, Poetry, Sentry

Our [Testing](#testing) documentation outlines how to run various tests, including unit and integration tests, and interpret the results. It also guides users through setting up a dedicated testing environment.
***
Get Started:

Clone the repository:
- [Epic Events](https://github.com/TMee3/DA-PYTHON-12)
$ git clone https://github.com/TMee3/DA-PYTHON-12.git



#### 🔧 Virtual Environment & Modules

For installing modules:
$ poetry install

Activating the virtual environment :
$ poetry shell

Deactivating the virtual environment:
$ deactivate

#### 🔧 Environment Configuration

Create and configure env_ex.txt to .env

Your setup is complete! 🎉


### 🔑 How to Use

Initial Setup: 🚀
To set up the system with an initialized database, configured .env file, installed modules, and an active environment, run the following command:


$ poetry run python epic_events/init_data.py
Starting the Application: 🌟
To start the Epic Events application, use the following command:


$ python3 -m epic_events
For Main Command Help: ❓
If you need help with the main command, you can run:


$ python3 -m epic_events --help
For Assistance with Specific Commands: ℹ️
For assistance with specific commands, such as the "client" command, you can use the following format:


$ python3 -m epic_events client --help
Logging In: 🔑
To log in, use the following command, replacing {your_email} with your actual email address:


$ python3 -m epic_events auth login -e {your_email}
Command Options (post-login): 📝
Once you are logged in, you can access various command options. For example, to create a contract, you can run:


$ python3 -m epic_events contract create --help
Logging Out: 🚪
To log out from your Epic Events account, use the following command:

$ python3 -m epic_events auth logout

### 🧪 Testing

To Run Tests:
$ pytest

Generating Flake 8 Report:
$ flake8

Viewing Coverage Reports:
$ coverage run -m pytest
$ coverage report
$ coverage html

### 🛠️ Sentry Monitoring

Sentry provides robust error tracking and logs significant actions like user and contract management.





The [Sentry Monitoring](#sentry-monitoring) section details the integration of Sentry for real-time issue tracking and resolution, illustrating how it enhances the CRM's reliability and performance.

### 📋 Frequently Asked Questions (FAQ)
---
In this section, find answers to common queries about Epic Events CRM. For additional support, contact our team at [support@epicevents.com](mailto:support@epicevents.com).

### 🤝 Contributing
---
Contributions are welcome! See our contribution guidelines for coding standards, pull request procedures, and more.

### ©️ Licensing
---
Epic Events CRM is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the LICENSE file for more details.