Tachbel Hostel Management System
Developed by Regina Kariuki

A comprehensive hostel management system designed for UNiversity students, featuring student registration, room booking, complaint management, and reporting. Built with Python, SQLAlchemy, and Click for CLI operations.

✨ Features
✅ Student Management

Register new students with  phone validation (07XXXXXXXX)

View, update, and delete student records

Track student bookings

✅ Room Management

Add, list, and modify rooms with pricing in KES

Track occupancy and availability

✅ Booking System

Book rooms for students with check-in/check-out dates

Cancel bookings and update occupancy

✅ Complaint Handling

File complaints assigned to managers

Track status (Open, In-Progress, Resolved)

✅ Reports & Analytics

Room occupancy percentages

Complaint resolution tracking

Financial summaries (revenue in KES)

🛠 Technologies Used
Backend: Python 3.8+

Database: SQLite (SQLAlchemy ORM)

CLI Framework: Click

Migrations: Alembic

Environment Management: Pipenv

🚀 Setup Instructions
Prerequisites
Python 3.8+

Pipenv (pip install pipenv)

Installation
Clone the repository:

bash
git clone https://github.com/yourusername/hostel-management-system.git
cd hostel-management-system
Set up the virtual environment and install dependencies:

bash
pipenv install
pipenv shell
Initialize the database:

bash
python -m lib.cli initdb
Run the application:

bash
# Command-line mode
python -m lib.cli student add --name "John Doe" --email "john@example.com" --phone "0712345678"

# Interactive menu mode
python -m lib.cli menu

📞 Support & Contact
For issues or feature requests:

Email: wanjiruregina678@gmail.com

🌟 Happy Hostel Management System!
You are all welcome to our hostels

📝 License
This project is open-source and free to use for learning purposes.