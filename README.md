Campus Resource Optimizer
Project by Team Laksha Cracker Developed for the CODE@FROST Hackathon | Blizzard Ops Track

❄️ Project Overview
The Campus Resource Optimizer is a real-time scheduling platform designed to eliminate administrative bottlenecks at educational institutions. It solves the problem of resource conflict (double-bookings) and ensures that students and faculty can access labs, seminar halls, and equipment efficiently.

🚀 Key Features
Conflict Resolution Algorithm: Prevents overlapping bookings for the same time slot.

Role-Based Access Control:

Teachers: Can book any resource instantly.

Students: Can book labs easily but must provide a mandatory "Purpose of Booking" for high-value seminar halls.

Arctic Search & Filter: Instant search by requirement tags (e.g., "AC", "Projector", "GPU").

Automated Confirmations: Integrated with Flask-Mail to send instant email receipts to users.

Glassmorphism UI: A high-contrast, colorful interface optimized for modern browsers.

🛠️ Tech Stack
Backend: Python / Flask

Database: SQLite (SQLAlchemy ORM)

Frontend: Bootstrap 5, Jinja2, Custom CSS

Email Service: Flask-Mail (SMTP)

📦 Local Setup Instructions
To run this project on your local machine:

Clone the Repository:

Bash

git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
Install Dependencies:

Bash

pip install flask flask-sqlalchemy flask-mail
Configure Email: Update the MAIL_USERNAME and MAIL_PASSWORD in app.py with your credentials.

Run the Application:

Bash

python app.py
Access the app at http://127.0.0.1:5000.
