import requests
import threading
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import pyqtSignal, QObject

class PerformanceWorker(QObject):
    finished = pyqtSignal(list)

    def fetch_performances(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.finished.emit(data)
        except Exception as e:
            print(f"Error fetching performances: {e}")
            self.finished.emit([])

class ViewPerformancesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Performances & Charts")
        self.performances_data = [] 
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
                background-color: #4CAF50; color: white; padding: 15px 32px;
                text-align: center; font-size: 16px; margin: 4px 2px; border-radius: 5px;
            }
            QPushButton:hover { background-color: #3e8e41; }
            #BtnChart { background-color: #007BFF; } #BtnChart:hover { background-color: #0056b3; }
        """)
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Performance ID", "File ID", "Algorithm ID", "Key ID", "Operation Type",
            "Execution Time (ms)", "Memory Usage (MB)", "Success", "Error Message", "Timestamp"
        ])
        layout.addWidget(self.table)

        button_layout = QHBoxLayout() 

        self.btn_chart = QPushButton("Generate Performance Chart", self)
        self.btn_chart.setObjectName("BtnChart") 
        self.btn_chart.clicked.connect(self.generate_chart)
        button_layout.addWidget(self.btn_chart)

        self.btn_back = QPushButton("Back", self)
        self.btn_back.clicked.connect(self.close)
        button_layout.addWidget(self.btn_back)

        layout.addLayout(button_layout) 
        self.setLayout(layout)

    def load_data(self):
        url = "http://localhost:8000/performance/" 
        self.worker = PerformanceWorker()
        self.worker.finished.connect(self.populate_table)
        thread = threading.Thread(target=self.worker.fetch_performances, args=(url,))
        thread.start()

    def populate_table(self, performances):
        self.performances_data = performances 
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
        self.table.resizeColumnsToContents()

    def generate_chart(self):
        """Generează și afișează o diagramă de performanță."""
        if not self.performances_data:
            QMessageBox.warning(self, "No Data", "No performance data available to generate a chart.")
            return

        if not pd or not plt:
            QMessageBox.critical(self, "Missing Libraries", "Please install pandas and matplotlib to generate charts (`pip install pandas matplotlib`).")
            return

        try:
            df = pd.DataFrame(self.performances_data)

            df['execution_time_ms'] = pd.to_numeric(df['execution_time_ms'], errors='coerce')
            df['memory_usage_mb'] = pd.to_numeric(df['memory_usage_mb'], errors='coerce')
            df = df.dropna(subset=['execution_time_ms', 'memory_usage_mb']) 

            avg_performance = df.groupby(['algorithm_id', 'operation_type']).agg(
                avg_time=('execution_time_ms', 'mean'),
                avg_mem=('memory_usage_mb', 'mean')
            ).reset_index()

            if avg_performance.empty:
                 QMessageBox.warning(self, "No Data", "Not enough valid data to plot.")
                 return

            avg_performance['label'] = avg_performance['algorithm_id'].astype(str) + ' - ' + avg_performance['operation_type']

            fig, ax1 = plt.subplots(figsize=(12, 7))

            color = 'tab:red'
            ax1.set_xlabel('Algorithm - Operation')
            ax1.set_ylabel('Average Execution Time (ms)', color=color)
            ax1.bar(avg_performance['label'], avg_performance['avg_time'], color=color, alpha=0.6, label='Avg Time (ms)')
            ax1.tick_params(axis='y', labelcolor=color)
            plt.xticks(rotation=45, ha="right")

            ax2 = ax1.twinx()  
            color = 'tab:blue'
            ax2.set_ylabel('Average Memory Usage (MB)', color=color)
            ax2.plot(avg_performance['label'], avg_performance['avg_mem'], color=color, marker='o', linestyle='--', label='Avg Memory (MB)')
            ax2.tick_params(axis='y', labelcolor=color)

            fig.tight_layout()
            plt.title('Average Performance Comparison')
            plt.show() 

        except Exception as e:
            QMessageBox.critical(self, "Chart Error", f"An error occurred while generating the chart: {e}")