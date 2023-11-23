import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,QLineEdit,  QPushButton, QLabel, QTableWidget, \
    QTableWidgetItem, QHeaderView, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage, QIcon, QColor
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy,QVBoxLayout, QGroupBox, QFormLayout
import cv2
import mysql.connector

class LoginButtonWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_window = None
        self.init_ui()

    def init_ui(self):
        box_layout = QVBoxLayout()
        icms_heading = QLabel("<font size='6' color='#333333'>ICMS</font>")
        icms_heading.setAlignment(Qt.AlignCenter)

        email_label = QLabel("Email:")
        password_label = QLabel("Password:")
        email_edit = QLineEdit()
        password_edit = QLineEdit()
        password_edit.setEchoMode(QLineEdit.Password)

        login_button = QPushButton('Login', self)
        login_button.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; border: 2px solid #3498db; "
            "border-radius: 5px; padding: 5px; font-size: 16px; }"
            "QPushButton:hover { background-color: #2980b9; }"
        )

        face_detection_button = QPushButton('Login with Face Detection', self)
        face_detection_button.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; border: 2px solid #3498db; "
            "border-radius: 5px; padding: 5px; font-size: 16px; }"
            "QPushButton:hover { background-color: #2980b9; }"
        )
        face_detection_button.clicked.connect(self.show_main_window)

        box_layout.addWidget(icms_heading, alignment=Qt.AlignCenter)
        box_layout.addWidget(email_label, alignment=Qt.AlignCenter)
        box_layout.addWidget(email_edit, alignment=Qt.AlignCenter)
        box_layout.addWidget(password_label, alignment=Qt.AlignCenter)
        box_layout.addWidget(password_edit, alignment=Qt.AlignCenter)
        box_layout.addWidget(login_button, alignment=Qt.AlignCenter)
        box_layout.addWidget(face_detection_button, alignment=Qt.AlignCenter)

        self.setLayout(box_layout)
        self.setWindowTitle('Login Button Window')
        self.setGeometry(200, 200, 400, 300)

    def show_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="18hc1495",
            database="facedetection"
        )
        self.db_cursor = self.db_connection.cursor()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera)
        self.timer.start(30)

    def init_ui(self):
        self.setWindowIcon(QIcon('Icon.png'))
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

        self.login_button = QPushButton('Login', self)
        self.logout_button = QPushButton('Logout', self)
        self.logout_button.setEnabled(False)

        self.personal_info_label = QLabel('Welcome!')
        self.course_info_label = QLabel('ICMS')

        self.camera_label = QLabel(self)
        self.logo_label = QLabel(self)
        self.logo_label.setAlignment(Qt.AlignCenter)

        logo_pixmap = QPixmap('Icon.png')
        self.logo_label.setPixmap(logo_pixmap.scaledToHeight(100))

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.logout_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.personal_info_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.course_info_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.camera_label, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        self.login_button.clicked.connect(self.login)
        self.logout_button.clicked.connect(self.logout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Intelligent Course Management System')
        self.setGeometry(100, 100, 800, 600)
        self.show()

    def update_camera(self):
        ret, frame = self.cap.read()

        if not ret or frame is None:
            print("Error: Unable to read frame from the camera.")
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

        self.camera_label.setPixmap(QPixmap.fromImage(q_img))

    def login(self):
        self.camera_window = CameraWindow(self.cap, self.show_dashboard)
        self.camera_window.show()
        self.camera_window.start_face_detection(self.face_cascade, self.insert_login_record, self.on_login_successful)

    def insert_login_record(self, student_name):
        try:
            query = "SELECT student_id FROM students WHERE name = %s"
            self.db_cursor.execute(query, (student_name,))
            result = self.db_cursor.fetchone()

            if result:
                student_id = result[0]
                course_id = 1
                query = "INSERT INTO loginhistory (student_id, course_id) VALUES (%s, %s)"
                values = (student_id, course_id)

                self.db_cursor.execute(query, values)
                self.db_connection.commit()
                print("Login record inserted successfully!")
            else:
                print("Student not found.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def on_login_successful(self, student_name):
        self.login_button.setEnabled(False)
        self.logout_button.setEnabled(True)
        self.personal_info_label.setText(f'Welcome, {student_name}!')

    def logout(self):
        self.login_button.setEnabled(True)
        self.logout_button.setEnabled(False)
        self.personal_info_label.setText('Welcome!')
        self.course_info_label.setText('ICMS.')

    def show_dashboard(self, student_name):
        self.dashboard_window = DashboardWindow(student_name, self.show_timetable)
        self.dashboard_window.show()

    def show_timetable(self, student_name):
        self.timetable_window = TimetableWindow(student_name)
        self.timetable_window.show()

    def closeEvent(self, event):
        self.cap.release()
        self.db_cursor.close()
        self.db_connection.close()
        event.accept()


class CameraWindow(QWidget):
    def __init__(self, capture, show_dashboard_callback):
        super().__init__()
        self.init_ui()
        self.capture = capture
        self.face_cascade = None
        self.insert_login_record = None
        self.on_login_successful = None
        self.show_dashboard_callback = show_dashboard_callback

    def init_ui(self):
        self.camera_label = QLabel(self)
        self.camera_label.setFixedSize(640, 480)

        layout = QVBoxLayout(self)
        layout.addWidget(self.camera_label)

        self.setLayout(layout)

    def start_face_detection(self, face_cascade, insert_login_record, on_login_successful):
        self.face_cascade = face_cascade
        self.insert_login_record = insert_login_record
        self.on_login_successful = on_login_successful

    def showEvent(self, event):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.detect_face)
        self.timer.start(30)

    def detect_face(self):
        ret, frame = self.capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if len(faces) > 0:
            x, y, w, h = faces[0]
            student_name = "Shaheer Imran"

            self.insert_login_record(student_name)
            self.timer.stop()
            self.close()
            self.on_login_successful(student_name)
            self.show_dashboard_callback(student_name)
        else:
            self.on_no_face_detected()

    def on_no_face_detected(self):
        self.insert_login_record("No face Detected")
        self.timer.stop()
        self.close()
        self.on_login_successful("No face Detected")


class DashboardWindow(QWidget):
    def __init__(self, student_name, show_timetable_callback):
        super().__init__()
        self.student_name = student_name
        self.init_ui()
        self.show_timetable_callback = show_timetable_callback

    def init_ui(self):
        self.setStyleSheet("background-color: #f0f0f0;")
        font = QFont("Arial", 12)

        sidebar_layout = QVBoxLayout()

        logo_label = QLabel(self)
        logo_pixmap = QPixmap('icon.png')
        logo_label.setPixmap(logo_pixmap.scaledToHeight(300))
        logo_label.setAlignment(Qt.AlignCenter)

        icms_label = QLabel("<font size='6' color='#333333'>ICMS</font>")
        icms_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(logo_label)
        sidebar_layout.addWidget(icms_label)

        main_layout = QVBoxLayout()

        heading_label = QLabel(f"<font size='6'>Welcome, {self.student_name}!</font>")
        heading_label.setAlignment(Qt.AlignCenter)
        heading_label.setFont(font)

        dashboard1_label = QLabel("<font size='6'>DASHBOARD:</font>")
        dashboard1_label.setAlignment(Qt.AlignCenter)
        dashboard1_label.setFont(font)

        next_class_label = QLabel("<font size='5'>Next class:</font>")
        next_class_label.setAlignment(Qt.AlignCenter)
        next_class_label.setStyleSheet("margin-top: 20px;")

        course_details_label = QLabel("<font size='5'>Course Name: DATABASE DESIGN<br>Lecture Room: r201</font>")
        course_details_label.setAlignment(Qt.AlignCenter)
        course_details_label.setStyleSheet(
            "background-color: white; border: 2px solid #333333; padding: 10px; margin-top: 10px;")

        show_courses_button = QPushButton('Show Courses', self)
        show_courses_button.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; border: 2px solid #3498db; "
            "border-radius: 5px; padding: 5px; font-size: 16px; }"
            "QPushButton:hover { background-color: #2980b9; }"
        )
        show_courses_button.clicked.connect(self.show_courses)
        sidebar_layout.addWidget(show_courses_button)

        show_timetable_button = QPushButton('Show Timetable', self)
        show_timetable_button.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; border: 2px solid #4CAF50; "
            "border-radius: 5px; padding: 5px; font-size: 16px; }"
            "QPushButton:hover { background-color: #45a049; }"
        )
        show_timetable_button.clicked.connect(self.show_timetable)
        sidebar_layout.addWidget(show_timetable_button)

        main_layout.addWidget(heading_label)
        main_layout.addWidget(dashboard1_label)
        main_layout.addWidget(next_class_label)
        main_layout.addWidget(course_details_label)

        layout = QHBoxLayout(self)
        layout.addLayout(sidebar_layout)
        layout.addLayout(main_layout)

        self.setLayout(layout)
        self.setGeometry(200, 200, 800, 400)

    def show_timetable(self):
        self.show_timetable_callback(self.student_name)

    def show_courses(self):
        self.courses_window = CoursesWindow()
        self.courses_window.show()


class CoursesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        courses_group_box = QGroupBox("Available Courses")
        form_layout = QFormLayout()

        self.add_course_detail(form_layout, "Database", "Monday, Wednesday", "9:00 AM - 10:30 AM")
        self.add_course_detail(form_layout, "Programming Fundamentals", "Tuesday, Thursday", "1:00 PM - 2:30 PM")
        self.add_course_detail(form_layout, "Calculus", "Monday, Wednesday", "3:00 PM - 4:30 PM")
        self.add_course_detail(form_layout, "Linear Algebra", "Tuesday, Thursday", "10:00 AM - 11:30 AM")
        self.add_course_detail(form_layout, "Maths", "Friday", "2:00 PM - 3:30 PM")

        courses_group_box.setLayout(form_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(courses_group_box, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
        self.setWindowTitle('Courses')
        self.setGeometry(200, 200, 400, 300)

class CoursesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        courses_group_box = QGroupBox("Available Courses")
        form_layout = QFormLayout()
        self.add_course_detail(form_layout, "Database", "Monday, Wednesday", "9:00 AM - 10:30 AM")
        self.add_course_detail(form_layout, "Programming Fundamentals", "Tuesday, Thursday", "1:00 PM - 2:30 PM")
        self.add_course_detail(form_layout, "Calculus", "Monday, Wednesday", "3:00 PM - 4:30 PM")
        self.add_course_detail(form_layout, "Linear Algebra", "Tuesday, Thursday", "10:00 AM - 11:30 AM")
        self.add_course_detail(form_layout, "Maths", "Friday", "2:00 PM - 3:30 PM")
        courses_group_box.setLayout(form_layout)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(courses_group_box, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)
        self.setWindowTitle('Courses')
        self.setGeometry(200, 200, 400, 300)

    def add_course_detail(self, layout, course_name, days, time):
        course_name_label = QLabel(f"<font size='5'>{course_name}</font>")
        days_label = QLabel(f"<b>Days:</b> {days}")
        time_label = QLabel(f"<b>Time:</b> {time}")
        layout.addRow(course_name_label, days_label)
        layout.addRow(time_label, QLabel())

class TimetableWindow(QWidget):
    def __init__(self, student_name):
        super().__init__()
        self.student_name = student_name
        self.init_ui()

    def init_ui(self):
        self.timetable_label = QLabel(f"Timetable for {self.student_name}", self)
        self.timetable_table = QTableWidget(self)
        self.timetable_table.setRowCount(6)
        self.timetable_table.setColumnCount(7)
        self.timetable_table.setHorizontalHeaderLabels(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
        self.timetable_table.verticalHeader().setVisible(False)
        self.timetable_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout = QVBoxLayout(self)
        layout.addWidget(self.timetable_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.timetable_table)
        self.setLayout(layout)
        self.setup_timetable()
        self.setWindowTitle('Timetable')
        self.setGeometry(200, 200, 800, 400)

    def setup_timetable(self):
        timetable_data = {
            "9:00 AM - 11:00 AM": ["Maths", "", "", "", "", ""],
            "1:00 PM - 3:00 PM": ["", "", "Database", "", "", ""],
            "10:00 AM - 12:00 PM": ["", "", "", "", "", ""],
            "No classes": ["", "", "", "", "", ""],
            "2:00 PM - 4:00 PM": ["", "Computer", "", "", "", ""],
        }

        for row, (time, courses) in enumerate(timetable_data.items()):
            time_item = QTableWidgetItem(time)
            self.timetable_table.setItem(row, 0, time_item)

            for col, course_info in enumerate(courses):
                item = QTableWidgetItem(course_info)
                if "No classes" in course_info:
                    item.setBackground(QColor(200, 200, 200))
                self.timetable_table.setItem(row, col + 1, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_button_window = LoginButtonWindow()
    login_button_window.show()
    sys.exit(app.exec_())



