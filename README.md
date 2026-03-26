# 🚍 Secure Public Transport Ticket System

A secure web-based ticket booking system built using Flask, implementing encryption, QR code validation, fraud detection, and HTTPS simulation.

---

## 📌 Project Overview

This project is designed to provide a secure and efficient public transport ticket booking system. It focuses on data security, user authentication, and validation mechanisms.

---

## 🎯 Features

- 🔐 User Registration & Login (Password Hashing)
- 🗄️ Secure Database Storage using SQLite
- 🎟️ Ticket Booking System
- 🔒 Ticket Data Encryption (Fernet Symmetric Encryption)
- 📱 QR Code Generation for Tickets
- ✅ Ticket Validation System
- 🚨 Fraud Detection (Rule-Based)
- 🌐 HTTPS Secure Communication (Simulation)

---

## 🧠 Technologies Used

- Python
- Flask
- SQLite
- HTML
- Cryptography (Fernet)
- Hashlib (SHA-256)
- QRCode Library

---

## 🔐 Security Features

### 1. Password Security (CO1)
- Passwords are hashed using SHA-256 before storing.

### 2. Ticket Data Protection (CO2)
- Ticket details are encrypted using symmetric encryption (Fernet).

### 3. QR Code Validation (CO3)
- Unique QR code is generated for each ticket.
- Ticket is validated using Ticket ID.

### 4. Fraud Detection (CO4)
- Rule-based system prevents invalid bookings (same source & destination).

### 5. Secure Communication (CO4)
- HTTPS simulation using SSL context in Flask.

---

## 🧱 Project Structure
SecureTicketSystem/

├── app.py
├── database.db
├── templates/
│ ├── index.html
│ ├── register.html
│ ├── login.html
│ ├── dashboard.html
│ ├── book.html
│ └── validate.html
│
├── static/
│ └── ticket_*.png

---

## 🚀 How to Run the Project

1. Clone the repository:

git clone https://github.com/your-username/Secure-Public-Transport-Ticket-System.git


2. Navigate to project folder:

cd SecureTicketSystem


3. Install dependencies:

pip install flask cryptography qrcode pillow


4. Run the application:

py app.py


5. Open in browser:

https://127.0.0.1:5000


---

## 🧠 System Workflow

1. User registers → password is hashed  
2. User logs in → credentials verified  
3. User books ticket → data encrypted  
4. Ticket stored in database  
5. QR code generated  
6. Ticket validated using ID  
7. Fraud detection rules applied  

---

## 🎓 SDG Alignment

This project supports **SDG 9: Industry, Innovation and Infrastructure** by promoting secure digital systems in transportation.

---

## 🏆 Conclusion

This system demonstrates secure application development using encryption, authentication, and validation techniques, making it suitable for real-world ticketing systems.

---

## 👩‍💻 Author

**Ashlesha Badgujar**
