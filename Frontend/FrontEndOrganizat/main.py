import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor
from manage_algorithms import ManageAlgorithmsWindow
from manage_keys import ManageKeysWindow
from manage_files import ManageFilesWindow
from view_performances import ViewPerformancesWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Local File Management - SI Proiect')
        self.setFixedSize(1000, 700)
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 1, 1)
        gradient.setColorAt(0, QColor(238, 250, 253))
        gradient.setColorAt(1, QColor(200, 220, 250))

        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px 32px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3e8e41;
            }
        """)

        self.titlu = QLabel('Local File Management', self)
        self.titlu.setStyleSheet("font-size: 43px; font-weight: bold; text-align: center;")
        self.titlu.setFixedWidth(500)
        self.titlu.setFixedHeight(100)

        self.subtitlu = QLabel('The safest place for your files.', self)
        self.subtitlu.setStyleSheet("font-size: 23px; font-weight: bold; text-align: center;")
        self.subtitlu.setFixedWidth(500)

        self.copyrightt = QLabel('© SI 2025 \nApetroaei Cezar-Stefan\nSimion Iustin-Denis\nAnastasiei Narcis-Stefan', self)
        self.copyrightt.setStyleSheet("font-size: 11px; font-weight: bold; text-align: center;")
        self.copyrightt.setFixedWidth(500)

        layout = QVBoxLayout()
        layout.addWidget(self.titlu)
        layout.addWidget(self.subtitlu)

        self.btn_manage_algorithms = QPushButton("Manage Algorithms", self)
        self.btn_manage_algorithms.clicked.connect(self.open_manage_algorithms)
        layout.addWidget(self.btn_manage_algorithms)

        self.btn_manage_keys = QPushButton("Manage Keys", self)
        self.btn_manage_keys.clicked.connect(self.open_manage_keys)
        layout.addWidget(self.btn_manage_keys)

        self.btn_manage_files = QPushButton("Manage Files", self)
        self.btn_manage_files.clicked.connect(self.open_manage_files)
        layout.addWidget(self.btn_manage_files)

        self.btn_view_performances = QPushButton("View Performances", self)
        self.btn_view_performances.clicked.connect(self.open_view_performances)
        layout.addWidget(self.btn_view_performances)

        
        layout.addWidget(self.copyrightt)
        self.setLayout(layout)

    def open_manage_algorithms(self):
        self.algorithms_window = ManageAlgorithmsWindow()
        self.algorithms_window.show()

    def open_manage_keys(self):
        self.keys_window = ManageKeysWindow()
        self.keys_window.show()

    def open_manage_files(self):
        self.files_window = ManageFilesWindow()
        self.files_window.show()

    def open_view_performances(self):
        self.performances_window = ViewPerformancesWindow()
        self.performances_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
