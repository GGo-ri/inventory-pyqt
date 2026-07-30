from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QSizePolicy)
from PyQt5.QtCore import Qt
from db_helper import DB, DB_CONFIG

class LoginDialog(QDialog) :
  def __init__(self, parent = None) :
    super().__init__(parent)
    self.setWindowTitle("로그인")
    self.resize(480, 200)

    self.db = DB(**DB_CONFIG)
    self.is_guest = False

    self.username = QLineEdit()
    self.username.setPlaceholderText("아이디")
    self.username.setFixedHeight(40)

    self.password = QLineEdit()
    self.password.setPlaceholderText("비밀번호")
    self.password.setEchoMode(QLineEdit.Password)
    self.password.setFixedHeight(40)
    self.password.returnPressed.connect(self.try_login)

    self.btn_login = QPushButton("로그인")
    self.btn_login.setFixedHeight(40)
    self.btn_login.clicked.connect(self.try_login)

    left_layout = QVBoxLayout()
    left_layout.addWidget(self.username)
    left_layout.addWidget(self.password)
    left_layout.addWidget(self.btn_login)

    self.btn_guest = QPushButton("GUEST\nLOGIN")
    self.btn_guest.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.btn_guest.setStyleSheet("font-weight : bold; font-size : 14px;")
    self.btn_guest.setFocusPolicy(Qt.NoFocus)
    self.btn_guest.clicked.connect(self.try_guest)

    main_layout = QHBoxLayout()
    main_layout.addLayout(left_layout, stretch = 3)
    main_layout.addWidget(self.btn_guest, stretch = 2)

    self.setLayout(main_layout)

    self.username.setFocus()

  def try_login(self) :
    uid = self.username.text().strip()
    pw = self.password.text().strip()

    if not uid or not pw :
      QMessageBox.warning(self, "오류", "아이디와 비밀번호 모두 입력하세요.")
      return

    ok = self.db.verify_user(uid, pw)
    if ok :
      self.is_guest = False
      self.accept()
    else :
      QMessageBox.critical(self, "실패", "아이디 또는 비밀번호가 올바르지 않습니다.")

  def try_guest(self) :
    self.is_guest = True
    self.accept()