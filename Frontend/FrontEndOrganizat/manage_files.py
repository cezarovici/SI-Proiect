import requests
import threading
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import pyqtSignal, QObject

class FileWorker(QObject):
    finished = pyqtSignal(list)

    def fetch_files(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()  # presupunem că API-ul returnează listă de dict-uri
            self.finished.emit(data)
        except Exception as e:
            print(f"Error fetching files: {e}")
            self.finished.emit([])

class ManageFilesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Files")
        self.init_ui()
        self.load_data()

    def init_ui(self):
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

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "File ID", 
            "Original Path", 
            "Encrypted Path", 
            "Original Hash", 
            "Encrypted Hash", 
            "Algorithm ID", 
            "Key ID", 
            "Encryption Date", 
            "Last Access"
        ])

        layout.addWidget(self.table)

        self.btn_back = QPushButton("Back", self)
        self.btn_back.clicked.connect(self.close)
        layout.addWidget(self.btn_back)

        hbox1 = QHBoxLayout()
        self.btn_addfile = QPushButton("Add a file", self)
        hbox1.addWidget(self.btn_addfile)

        self.btn_deletefile = QPushButton("Delete a file", self)
        hbox1.addWidget(self.btn_deletefile)
        layout.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        self.btn_encrfile = QPushButton("Encrypt", self)
        hbox2.addWidget(self.btn_encrfile)

        self.btn_decrfile = QPushButton("Decrypt", self)
        hbox2.addWidget(self.btn_decrfile)
        layout.addLayout(hbox2)

        self.setLayout(layout)

    def load_data(self):
        url = "http://localhost:8000/files"  # schimbă cu API-ul tău real

        self.worker = FileWorker()
        self.worker.finished.connect(self.populate_table)

        thread = threading.Thread(target=self.worker.fetch_files, args=(url,))
        thread.start()

    def populate_table(self, files):
        self.table.setRowCount(len(files))
        for i, file in enumerate(files):
            self.table.setItem(i, 0, QTableWidgetItem(str(file.get("file_id", ""))))
            self.table.setItem(i, 1, QTableWidgetItem(file.get("original_path", "")))
            self.table.setItem(i, 2, QTableWidgetItem(file.get("encrypted_path", "")))
            self.table.setItem(i, 3, QTableWidgetItem(file.get("original_hash") or "N/A"))
            self.table.setItem(i, 4, QTableWidgetItem(file.get("encrypted_hash") or "N/A"))
            self.table.setItem(i, 5, QTableWidgetItem(str(file.get("algorithm_id", ""))))
            self.table.setItem(i, 6, QTableWidgetItem(str(file.get("key_id", ""))))
            self.table.setItem(i, 7, QTableWidgetItem(file.get("encryption_date", "")))
            self.table.setItem(i, 8, QTableWidgetItem(file.get("last_access") or "N/A"))
