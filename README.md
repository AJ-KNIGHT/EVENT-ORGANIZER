# 🎉 Event Management System

This is a modern and user-friendly **Event Management System** built with **Django** and **Bootstrap**. It allows users to browse, book, and manage events seamlessly while providing an intuitive admin dashboard for event organizers.

## 🌟 Key Features

### 🖥️ User Side
- 🔍 Browse and search events.
- 📅 Book events with custom date and venue options.
- 💰 Choose payment method: **UPI/QR code** or **Cash on Event Day**.
- 📝 Submit change requests for booked events (venue, date, etc.).
- 📩 Receive email notifications for booking confirmations.

### ⚙️ Admin Side
- 🎛️ Manage events, bookings, and user requests via Django Admin.
- 📬 Get notified when a booking or change request is submitted.
- 📊 View booking details, user information, and payment status.

## 🛠️ Installation

Follow these steps to set up the project locally:

1. **Clone the Repository:**
```bash
git clone https://github.com/AJ-KNIGHT/EVENT-ORGANIZER.git
cd event-management-system
```

2. **Create a Virtual Environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables:**
Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

5. **Apply Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create Superuser (Admin Account):**
```bash
python manage.py createsuperuser
```

7. **Run the Development Server:**
```bash
python manage.py runserver
```
Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📸 Project Screenshots

- 🎥 **Home Page:** Full-page video background with transparent navbar.
- 📅 **Booking Form:** Clean, modern form with user-friendly inputs.
- 🖱️ **Dashboard:** Manage bookings, payments, and change requests.

## 📦 Project Structure
```
├── eventapp         # Event-related models, views, templates
├── userapp          # User authentication and profile management
├── paymentapp       # Payment and booking-related functionalities
├── templates        # All frontend templates (Bootstrap-based)
├── static           # CSS, JS, images, and videos
├── manage.py        # Django management script
└── README.md        # Project documentation
```

## 🚀 Future Enhancements
- 📱 Add responsive mobile views.
- 📜 Generate booking receipts.
- 🔔 Real-time notifications for admin and users.

## 🙌 Credits
- **Django** - Backend Framework
- **Bootstrap** - Frontend Styling
- **Pexels** - Free background video assets

## 📜 License
This project is licensed under the **MIT License**. Feel free to use and modify it.

## 📞 Contact
For any queries or suggestions, contact:
- ✉️ Email: eventpro49@gmail.com
- 🌐 Project GitHub: [https://github.com/AJ-KNIGHT/EVENT-ORGANIZER](https://github.com/AJ-KNIGHT/EVENT-ORGANIZER)

---
🚀 Made with ❤️ by **Happy Hours**

