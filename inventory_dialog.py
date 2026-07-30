from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QSpinBox, QPushButton, QMessageBox, QLabel)
from PyQt5.QtCore import Qt
from db_helper import DB, DB_CONFIG

class InventoryDialog(QDialog) :
  def __init__(self, mode = "add", jersey_id = None, product_name = "", current_stock = 0, is_admin = False, parent = None) :
    super().__init__(parent)
    self.mode = mode
    self.jersey_id = jersey_id
    self.is_admin = is_admin
    self.db = DB(**DB_CONFIG)

    self.team_codes = {
      "맨체스터 시티(Manchester City)" : "10",
      "리버풀(Liverpool)" : "20",
      "애스턴 빌라(Aston Villa)" : "30",
      "첼시(Chelsea)" : "40",
      "아스널(Arsenal)" : "50",
      "맨체스터 유나이티드(Manchester United)" : "60",
    }

    self.type_codes = {"HOME" : "01", "AWAY" : "02"}

    if self.mode == "add" :
      self.setWindowTitle("신규 유니폼 등록")
      self.resize(380, 280)
    else :
      self.setWindowTitle("재고 수량 수정")
      self.resize(300, 150)

    self.init_ui(product_name, current_stock)

  def init_ui(self, product_name, current_stock) :
    layout = QVBoxLayout()
    form_layout = QFormLayout()

    if self.mode == "add" :
      self.combo_team = QComboBox()
      self.combo_team.addItems(list(self.team_codes.keys()))

      self.input_back_num = QSpinBox()
      self.input_back_num.setRange(1, 99)

      self.input_name = QLineEdit()
      self.input_name.setPlaceholderText("예: 엘링 홀란")

      self.combo_type = QComboBox()
      self.combo_type.addItems(list(self.type_codes.keys()))

      self.input_stock = QSpinBox()
      self.input_stock.setRange(0, 9999)
      self.input_stock.setValue(1)

      self.input_price = QSpinBox()
      self.input_price.setRange(0, 10000000)
      self.input_price.setSingleStep(10000)
      self.input_price.setValue(195000)

      form_layout.addRow("팀 선택 : ", self.combo_team)
      form_layout.addRow("등번호 : ", self.input_back_num)
      form_layout.addRow("선수명 : ", self.input_name)
      form_layout.addRow("유니폼 종류 : ", self.combo_type)
      form_layout.addRow("수량 : ", self.input_stock)
      form_layout.addRow("가격(원) : ", self.input_price)

    elif self.mode == "edit_stock" :
      self.lbl_info = QLabel(f"<b>제품명 : </b> {product_name}")
      layout.addWidget(self.lbl_info)

      self.input_stock = QSpinBox()
      self.input_stock.setRange(0, 9999)
      self.input_stock.setValue(current_stock)

      form_layout.addRow("수량 변경 : ", self.input_stock)

    layout.addLayout(form_layout)

    btn_layout = QHBoxLayout()
    self.btn_save = QPushButton("저장")
    self.btn_cancle = QPushButton("취소")

    self.btn_save.clicked.connect(self.save_data)
    self.btn_cancle.clicked.connect(self.reject)

    btn_layout.addWidget(self.btn_save)
    btn_layout.addWidget(self.btn_cancle)
    layout.addLayout(btn_layout)

    self.setLayout(layout)

  def generate_serial_number(self, team_display_name, j_type, back_num) :
    t_code = self.team_codes.get(team_display_name, "10")
    type_code = self.type_codes.get(j_type, "01")
    num_code = f"{back_num:02d}"

    return f"{t_code}{type_code}{num_code}"

  def save_data(self) :
    if self.mode == "add" :
      selected_team = self.combo_team.currentText()
      back_num = self.input_back_num.value()
      player_name = self.input_name.text().strip()
      j_type = self.combo_type.currentText()
      stock = self.input_stock.value()
      price = self.input_price.value()

      if not player_name :
        QMessageBox.warning(self, "경고", "선수명을 입력해 주세요.")
        return

      serial_number = self.generate_serial_number(selected_team, j_type, back_num)

      korean_team_name = selected_team.split("(")[0].strip()
      full_product_name = f"{korean_team_name} {player_name}".strip()

      ok = self.db.add_jersey(serial_number, back_num, full_product_name, j_type, stock, price, is_admin = self.is_admin,)

      if ok :
        QMessageBox.information(self, "성공", "유니폼이 성공적으로 등록되었습니다.")
        self.accept()
      else :
        QMessageBox.critical(self, "오류", "유니폼 등록에 실패했습니다.")

    elif self.mode == "edit_stock" :
      new_stock = self.input_stock.value()
      ok = self.db.update_stock(self.jersey_id, new_stock, is_admin = self.is_admin)

      if ok :
        QMessageBox.information(self, "성공", "수량이 수정되었습니다.")
        self.accept()
      else :
        QMessageBox.critical(self, "오류", "수량 수정에 실패했습니다.")