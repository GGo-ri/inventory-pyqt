import sys
from PyQt5.QtWidgets import QApplication
from login_dialog import LoginDialog
from main_window import MainWindow

def main() :
  app = QApplication(sys.argv)

  login_dialog = LoginDialog()

  if login_dialog.exec_() == LoginDialog.Accepted :
    is_admin = not login_dialog.is_guest

    main_window = MainWindow(is_admin = is_admin)
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__" :
  main()