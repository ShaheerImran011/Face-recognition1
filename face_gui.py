import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QDateTime

class StudentDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logo_label = QLabel(self)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setPixmap(QPixmap('Icon.png').scaledToWidth(200))
        logo_label.setScaledContents(True)

        student_name_label = QLabel("<font size='5' color='green'>Welcome, Shaheer Imran!</font>")
        student_name_label.setAlignment(Qt.AlignCenter)

        dashboard_heading = QLabel("<font size='6' color='green'>Dashboard</font>")
        dashboard_heading.setAlignment(Qt.AlignCenter)

        course_label = QLabel("<font size='5'>Current Course:</font> Computer Science")

        current_time = QDateTime.currentDateTime()
        upcoming_class_time = current_time.addSecs(3600)
        upcoming_class_label_text = f"<font size='5'>Upcoming Class:</font> Math 101 at {upcoming_class_time.toString('hh:mm AP')}"
        upcoming_class_label = QLabel(upcoming_class_label_text)

        time_label = QLabel("<font size='5'>Class Time:</font> 2:00 PM - 4:00 PM")

        main_layout = QVBoxLayout(self)

        top_layout = QVBoxLayout()
        top_layout.addWidget(logo_label)
        top_layout.addWidget(student_name_label)
        top_layout.addWidget(dashboard_heading)

        info_layout = QHBoxLayout()
        info_layout.addLayout(top_layout)

        left_layout = QVBoxLayout()
        left_layout.addWidget(course_label)
        left_layout.addWidget(upcoming_class_label)
        left_layout.addWidget(time_label)

        info_layout.addLayout(left_layout)
        main_layout.addLayout(info_layout)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

        self.setWindowTitle('Student Dashboard')
        self.setGeometry(100, 100, 600, 400)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentDashboard()
    sys.exit(app.exec_())
