# view_performances.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor

class ViewPerformancesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Performances")
        
        self.init_ui()

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

        # Exemplu de date modificate pentru a include toate câmpurile tabelei
        sample_performance = [
            {
                "performance_id": 1,
                "file_id": 1,
                "algorithm_id": 1,
                "key_id": 101,
                "operation_type": "encrypt",
                "execution_time_ms": 10.5,
                "memory_usage_mb": 20.3,
                "success": True,
                "error_message": None,
                "timestamp": "2025-05-20 00:30:00"
            },
            {
                "performance_id": 2,
                "file_id": 2,
                "algorithm_id": 2,
                "key_id": 102,
                "operation_type": "decrypt",
                "execution_time_ms": 12.8,
                "memory_usage_mb": 25.1,
                "success": False,
                "error_message": "Decryption failed: Invalid key.",
                "timestamp": "2025-05-20 00:35:00"
            }
        ]

        self.table.setRowCount(len(sample_performance))
        for i, perf in enumerate(sample_performance):
            self.table.setItem(i, 0, QTableWidgetItem(str(perf["performance_id"])))
            self.table.setItem(i, 1, QTableWidgetItem(str(perf["file_id"])))
            self.table.setItem(i, 2, QTableWidgetItem(str(perf["algorithm_id"])))
            self.table.setItem(i, 3, QTableWidgetItem(str(perf["key_id"])))
            self.table.setItem(i, 4, QTableWidgetItem(perf["operation_type"]))
            self.table.setItem(i, 5, QTableWidgetItem(str(perf["execution_time_ms"])))
            self.table.setItem(i, 6, QTableWidgetItem(str(perf["memory_usage_mb"])))
            self.table.setItem(i, 7, QTableWidgetItem("Success" if perf["success"] else "Failed"))
            self.table.setItem(i, 8, QTableWidgetItem(perf["error_message"] if perf["error_message"] else "N/A"))
            self.table.setItem(i, 9, QTableWidgetItem(perf["timestamp"]))

        layout.addWidget(self.table)


        self.btn_back = QPushButton("Back", self)
        self.btn_back.clicked.connect(self.close)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)
