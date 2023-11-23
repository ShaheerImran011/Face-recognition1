import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class StudentDetailsWindow(QDialog):
    def __init__(self, student_name, parent=None):
        super().__init__(parent)

        # Initialize UI components and layout
        self.init_ui(student_name)

    def init_ui(self, student_name):
        # Create labels to display student details
        name_label = QLabel(f"<font size='5'>Name:</font> {student_name}")
        id_label = QLabel("<font size='5'>Student ID:</font> 12345") 
        course_label = QLabel("<font size='5'>Course:</font> Computer Science") 

        # Create layout
        layout = QVBoxLayout(self)
        layout.addWidget(name_label, alignment=Qt.AlignCenter)
        layout.addWidget(id_label, alignment=Qt.AlignCenter)
        layout.addWidget(course_label, alignment=Qt.AlignCenter)

        # Set up the student details window
        self.setWindowTitle('Student Details')
        self.setGeometry(200, 200, 300, 200)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI components and layout
        self.init_ui()

    def init_ui(self):
        # Create login/logout buttons
        self.login_button = QPushButton('Login', self)
        self.logout_button = QPushButton('Logout', self)
        self.logout_button.setEnabled(False)  # Initially disable logout button

        # Create dynamic display area for personalized information
        self.personal_info_label = QLabel("<font size='6'>Welcome!</font>")

        # Create layout
        layout = QVBoxLayout(self)

        # Set background color for the main window
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray) 
        self.setPalette(p)

        # Add a heading label
        heading_label = QLabel("<font size='7' color='blue'>Intelligent Course Management System</font>")
        layout.addWidget(heading_label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.logout_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.personal_info_label, alignment=Qt.AlignCenter)

        # Connect button signals to functions
        self.login_button.clicked.connect(self.login)
        self.logout_button.clicked.connect(self.logout)  

        # Set up the main window
        self.setWindowTitle('Intelligent Course Management System')
        self.setGeometry(100, 100, 400, 300)
        self.show()

    def login(self):
        # Placeholder for login functionality
      
        student_name = "Shaheer Imran"  
        self.on_login_successful(student_name)

    def on_login_successful(self, student_name):
      
        self.login_button.setEnabled(False)
        self.logout_button.setEnabled(True)
        self.personal_info_label.setText(f"<font size='6'>Welcome, {student_name}!</font>")

        # Open student details window after successful login
        self.student_details_window = StudentDetailsWindow(student_name)
        self.student_details_window.exec_()

    def logout(self):
       
        self.login_button.setEnabled(True)
        self.logout_button.setEnabled(False)
        self.personal_info_label.setText("<font size='6'>Welcome!</font>")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())