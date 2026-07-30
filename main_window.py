import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView, QApplication, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QStackedWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget,
)
from db_helper import DB, DB_CONFIG
from inventory_dialog import InventoryDialog

class MainWindow(QMainWindow) :
  def __init__(self, is_admin = False) :
    super().__init__()
    self.is_admin = is_admin
    self.db = DB(**DB_CONFIG)
    self.current_team = None

    self.teams = [
      "맨체스터 시티(Manchester City)",
      "리버풀(Liverpool)",
      "애스턴 빌라(Aston Villa)",
      "첼시(Chelsea)",
      "아스널(Arsenal)",
      "맨체스터 유나이티드(Manchester United)",
    ]

    self.setWindowTitle(f"유니폼 재고 관리 시스템 ({'관리자 권한' if self.is_admin else '게스트 모드'})")
    self.resize(500, 650)

    self.stack = QStackedWidget()
    self.setCentralWidget(self.stack)

    self.page_team_select = self.create_team_select_page()
    self.page_jersey_list = self.create_jersey_list_page()

    self.stack.addWidget(self.page_team_select)
    self.stack.addWidget(self.page_jersey_list)

  # 팀 선택 화면
  def create_team_select_page(self) :
    page = QWidget()
    layout = QVBoxLayout()
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(12)

    title = QLabel("프리미어리그 팀 선택")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px")
    layout.addWidget(title)

    for team_name in self.teams:
      btn = QPushButton(team_name)
      btn.setFixedHeight(55)
      btn.setStyleSheet("""
          QPushButton {
              font-size: 15px;
              font-weight: bold;
              background-color: #f8f9fa;
              border: 1px solid #ced4da;
              border-radius: 8px;
          }
          QPushButton:hover {
              background-color: #e9ecef;
              border-color: #adb5bd;
          }
      """)
      btn.clicked.connect(lambda checked, name = team_name : self.open_team_jerseys(name))
      layout.addWidget(btn)

    page.setLayout(layout)
    return page

  # 팀별 유니폼 재고 목록 화면
  def create_jersey_list_page(self) :
    page = QWidget()
    layout = QVBoxLayout()
    layout.setContentsMargins(20, 20, 20, 20)

    header_layout = QHBoxLayout()

    self.btn_back = QPushButton("팀 선택 화면으로 돌아가기")
    self.btn_back.setFixedWidth(180)
    self.btn_back.clicked.connect(self.go_to_team_select)
    header_layout.addWidget(self.btn_back)

    self.lbl_team_title = QLabel("")
    self.lbl_team_title.setStyleSheet("font-size: 16px; font-weight: bold;")
    self.lbl_team_title.setAlignment(Qt.AlignCenter)
    header_layout.addWidget(self.lbl_team_title)

    layout.addLayout(header_layout)

    self.table = QTableWidget()
    self.table.setColumnCount(7)
    self.table.setHorizontalHeaderLabels(
      ["ID", "일련번호", "등번호", "제품명", "종류", "재고 수량", "가격(원)",]
    )

    self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.table.hideColumn(0)

    layout.addWidget(self.table)

    btn_layout = QHBoxLayout()

    self.btn_add = QPushButton("신규 유니폼 등록")
    self.btn_edit = QPushButton("재고 수량 수정")
    self.btn_delete = QPushButton("유니폼 삭제")

    self.btn_add.clicked.connect(self.open_add_dialog)
    self.btn_edit.clicked.connect(self.open_edit_dialog)
    self.btn_delete.clicked.connect(self.delete_jersey)

    btn_layout.addWidget(self.btn_add)
    btn_layout.addWidget(self.btn_edit)
    btn_layout.addWidget(self.btn_delete)

    if not self.is_admin :
      self.btn_add.setEnabled(False)
      self.btn_edit.setEnabled(False)
      self.btn_delete.setEnabled(False)

    layout.addLayout(btn_layout)
    page.setLayout(layout)
    return page

  # 화면 전환
  def open_team_jerseys(self, team_display_name) :
    self.current_team = team_display_name
    korean_team_name = team_display_name.split("(")[0].strip()
    self.lbl_team_title.setText(f"[{korean_team_name}] 유니폼 재고 현황")

    self.load_data()
    self.stack.setCurrentIndex(1)

  def go_to_team_select(self) :
    self.stack.setCurrentIndex(0)

  def load_data(self) :
    if not self.current_team :
      return

    korean_team_name = self.current_team.split("(")[0].strip()
    rows = self.db.get_jerseys(team = korean_team_name)

    rows = sorted(rows, key = lambda x: int(x[2]))

    self.table.setRowCount(0)
    for row_idx, row_data in enumerate(rows) :
      self.table.insertRow(row_idx)

      for col_idx, value in enumerate(row_data) :
        if col_idx == 6:
          item_text = f"{value:,}"
        else :
          item_text = str(value)

        item = QTableWidgetItem(item_text)
        item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row_idx, col_idx, item)

  # 유니폼 신규 등록
  def open_add_dialog(self) :
    korean_team_name = (self.current_team.split("(")[0].strip() if self.current_team else "")
    dialog = InventoryDialog(
      mode = "add",
      selected_team = korean_team_name,
      is_admin = self.is_admin,
      parent = self,
    )
    if dialog.exec_() :
      self.load_data()

  # 유니폼 재고 수정
  def open_edit_dialog(self) :
    selected_row = self.table.currentRow()
    if selected_row < 0 :
      QMessageBox.warning(self, "경고", "수정할 유니폼을 선택해 주세요.")
      return

    jersey_id = int(self.table.item(selected_row, 0).text())
    product_name = self.table.item(selected_row, 3).text()
    current_stock = int(self.table.item(selected_row, 5).text())

    dialog = InventoryDialog(
        mode = "edit_stock",
        jersey_id = jersey_id,
        product_name = product_name,
        current_stock = current_stock,
        is_admin = self.is_admin,
        parent = self,
    )
    if dialog.exec_() :
      self.load_data()

  # 유니폼 삭제
  def delete_jersey(self) :
    selected_row = self.table.currentRow()
    if selected_row < 0 :
      QMessageBox.warning(self, "경고", "삭제할 유니폼을 선택해 주세요.")
      return

    jersey_id = int(self.table.item(selected_row, 0).text())
    product_name = self.table.item(selected_row, 3).text()

    reply = QMessageBox.question(
      self,
      "삭제 확인",
      f"정말로 '{product_name}' 유니폼을 삭제하시겠습니까?",
      QMessageBox.Yes | QMessageBox.No,
      QMessageBox.No,
    )

    if reply == QMessageBox.Yes :
      ok = self.db.delete_jersey(jersey_id, is_admin = self.is_admin)
      if ok :
        QMessageBox.information(self, "성공", "삭제되었습니다.")
        self.load_data()
      else :
        QMessageBox.critical(self, "오류", "삭제에 실패했습니다.")

if __name__ == "__main__" :
  app = QApplication(sys.argv)

  window = MainWindow(is_admin = True)
  window.show()
  sys.exit(app.exec_())