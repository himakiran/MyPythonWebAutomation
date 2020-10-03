from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QLineEdit
import sys


def ask_password(arg_list):
    app = QApplication(arg_list)
    main_window = QMainWindow()
    main_window.setGeometry(400, 400, 200, 100)
    main_window.setWindowTitle("Enter Password !!")
    password, done = QInputDialog.getText(main_window, 'Input Dialog', 'Enter Password:', QLineEdit.Password)
    main_window.show()
    if done:
        return password
    sys.exit(app.exec_())


def ask_OTP(arg_list):
    app = QApplication(arg_list)
    main_window = QMainWindow()
    main_window.setGeometry(400, 400, 200, 100)
    main_window.setWindowTitle("Enter Your OTP !!")
    OTP, done = QInputDialog.getText(main_window, 'Input Dialog', 'Enter oNEtIM3p4SSW0RD:', QLineEdit.Password)
    main_window.show()
    if done:
        return OTP
    sys.exit(app.exec_())

