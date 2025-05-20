import requests
import threading
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import pyqtSignal, QObject

class PerformanceWorker(QObject):
    finished = pyqtSignal(list)

    def fetch_performances(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()  # presupunem că API-ul returnează listă de dict-uri
            self.finished.emit(data)
        except Exception as e:
            print(f"Error fetching performances: {e}")
            self.finished.emit([])

class ViewPerformancesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Performances")
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
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Performance ID",
            "File ID",
            "Algorithm ID",
            "Key ID",
            "Operation Type",
            "Execution Time (ms)",
            "Memory Usage (MB)",
            "Success",
            "Error Message",
            "Timestamp"
        ])

        layout.addWidget(self.table)

        self.btn_back = QPushButton("Back", self)
        self.btn_back.clicked.connect(self.close)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

    def load_data(self):
        url = "http://localhost:8000/performance"  # Schimbă cu URL-ul API-ului tău

        self.worker = PerformanceWorker()
        self.worker.finished.connect(self.populate_table)

        thread = threading.Thread(target=self.worker.fetch_performances, args=(url,))
        thread.start()

    def populate_table(self, performances):
        self.table.setRowCount(len(performances))
        for i, perf in enumerate(performances):
            self.table.setItem(i, 0, QTableWidgetItem(str(perf.get("performance_id", ""))))
            self.table.setItem(i, 1, QTableWidgetItem(str(perf.get("file_id", ""))))
            self.table.setItem(i, 2, QTableWidgetItem(str(perf.get("algorithm_id", ""))))
            self.table.setItem(i, 3, QTableWidgetItem(str(perf.get("key_id", ""))))
            self.table.setItem(i, 4, QTableWidgetItem(perf.get("operation_type", "")))
            self.table.setItem(i, 5, QTableWidgetItem(str(perf.get("execution_time_ms", ""))))
            self.table.setItem(i, 6, QTableWidgetItem(str(perf.get("memory_usage_mb", ""))))
            self.table.setItem(i, 7, QTableWidgetItem("Success" if perf.get("success") else "Failed"))
            self.table.setItem(i, 8, QTableWidgetItem(perf.get("error_message") or "N/A"))
            self.table.setItem(i, 9, QTableWidgetItem(perf.get("timestamp", "")))
