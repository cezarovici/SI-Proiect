import requests
import threading
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import pyqtSignal, QObject

class Worker(QObject):
    finished = pyqtSignal(list)

    def fetch_algorithms(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json() 
            self.finished.emit(data)
        except Exception as e:
            print(f"Error fetching data: {e}")
            self.finished.emit([])

class ManageAlgorithmsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Algorithms")
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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", 
            "Name", 
            "Type", 
            "Parameters", 
            "Created At", 
            "Updated At"
        ])
        layout.addWidget(self.table)

        self.btn_back = QPushButton("Back", self)
        self.btn_back.clicked.connect(self.close)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

    def load_data(self):
        url = "http://localhost:8000/algorithms/"

        self.worker = Worker()
        self.worker.finished.connect(self.populate_table)

        thread = threading.Thread(target=self.worker.fetch_algorithms, args=(url,))
        thread.start()

    def populate_table(self, algorithms):
        self.table.setRowCount(len(algorithms))
        for i, alg in enumerate(algorithms):
            self.table.setItem(i, 0, QTableWidgetItem(str(alg.get("algorithm_id", ""))))
            self.table.setItem(i, 1, QTableWidgetItem(alg.get("name", "")))
            self.table.setItem(i, 2, QTableWidgetItem(alg.get("type", "")))
            self.table.setItem(i, 3, QTableWidgetItem(alg.get("parameters", "")))
            self.table.setItem(i, 4, QTableWidgetItem(alg.get("created_at", "")))
            self.table.setItem(i, 5, QTableWidgetItem(alg.get("updated_at", "")))
