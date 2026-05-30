# AI – DRIVEN SMART SURVEILLANCE FOR WEAPON DETECTION USING YOLOv8

## Demo Video

[Watch Project Demo](https://youtu.be/vkhxaQHgLU0)

---

## Overview

The AI -  Driven Smart Surveillance for Weapon Detection Using YOLOv8 is a real-time surveillance and security application developed using YOLOv8, OpenCV, Django, and PyQt5. The system detects handguns from live webcam feeds and sends alerts through an integrated backend server.

This project was developed as a major academic project to improve public safety through intelligent monitoring and real-time threat detection.

---

## Features

- Real-time handgun detection using YOLOv8
- Live webcam monitoring
- PyQt5-based desktop application
- Django backend integration
- Automatic threat alert generation
- Real-time alert notifications through registered email or mobile number
- Detection frame capture and storage
- Detection log management
- Dashboard for viewing previous detection records

---

## Technologies Used

### Client Side Application
- Python
- PyQt5
- OpenCV
- YOLOv8

### Backend / Server Side
- Django
- Django REST Framework
- REST API Integration

### Machine Learning
- YOLOv8 Object Detection

---

## System Workflow

```plaintext
Webcam Feed
      ↓
YOLOv8 Handgun Detection
      ↓
Threat Alert Generation
      ↓
Email / Mobile Notification
      ↓
Detection Data Storage
      ↓
Dashboard Monitoring
```

---

## Project Structure

```plaintext
AI-Smart-Surveillance-System/
│
├── client_side/
│   ├── UI/
│   ├── alarms/
│   ├── detection.py
│   ├── main.py
│   └── requirements.txt
│
├── server_side/
│   ├── alertupload_rest/
│   ├── detection/
│   ├── wd_ss/
│   ├── manage.py
│   └── requirements.txt
│
├── README.md
└── .gitignore
```

---

## Screenshots

### Login Interface

<img width="317" height="352" alt="Login_ _Registration" src="https://github.com/user-attachments/assets/3be96045-bea4-430d-811f-9b26ecfd7786" />


---

### Detection Window

<img width="872" height="568" alt="Detection Window" src="https://github.com/user-attachments/assets/d20ee375-5eb5-4090-bc73-c9503ab29b3c" />

---

### Alert Notification System [Email & Mobile Alerts]

<img width="966" height="467" alt="Email Alert" src="https://github.com/user-attachments/assets/16578bd1-b837-4d29-b1d0-80da9c0e577f" />

<img width="1080" height="2412" alt="Mobile Alert" src="https://github.com/user-attachments/assets/735fb3ca-4435-4379-9a4b-ab4d2cf4a77c" />

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Prince-of-Morocco/AI-Smart-Surveillance-System.git
```

---

## Client Side Setup

```bash
cd client_side
pip install -r requirements.txt
```

Run Client Application:

```bash
python main.py
```

---

## Server Side Setup

```bash
cd server_side
pip install -r requirements.txt
```

Run Django Server:

```bash
python manage.py runserver
```

---

## Workflow

1. User logs into the desktop application
2. Webcam monitoring starts
3. YOLOv8 detects handguns in real time
4. Detected frames are sent to Django backend
5. Real-time alerts are sent through registered email or mobile number
6. Detection logs and monitoring records are stored
7. Users can access previous detection history through the dashboard

---

## Future Enhancements

- Expand detection capabilities to other threats such as explosives and dangerous objects
- Improve system adaptability for different surveillance environments
- Multi-camera monitoring support
- Cloud-based deployment and remote monitoring
- Mobile application integration
- Real-time analytics and monitoring dashboard
- Smart city and public safety integration

---

## Author

Kolloju Srinivas Bharath Raj

---

## Portfolio

Portfolio Website:
https://react-portfolio-ochre-gamma.vercel.app/

---

## Contact

For academic or project-related queries:

Email: bharathraj1024@gmail.com

---

## License

This project is developed for academic and educational purposes.
