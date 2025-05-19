# manage_algorithms.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor

class ManageAlgorithmsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Algorithms")
        
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

        # Creăm un tabel cu informații despre algoritmi; în practică vei lucra cu date din baza de date
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

        # Exemplu de date modificate pentru a include și câmpurile de timp
        sample_algorithms = [
            {
                "algorithm_id": 1, 
                "name": "AES", 
                "type": "symmetric", 
                "parameters": "key=256", 
                "created_at": "2025-05-20 00:00:00", 
                "updated_at": "2025-05-20 00:00:00"
            },
            {
                "algorithm_id": 2, 
                "name": "RSA", 
                "type": "asymmetric", 
                "parameters": "key=2048", 
                "created_at": "2025-05-20 00:00:00", 
                "updated_at": "2025-05-20 00:00:00"
            }
        ]

        self.table.setRowCount(len(sample_algorithms))
        for i, alg in enumerate(sample_algorithms):
            self.table.setItem(i, 0, QTableWidgetItem(str(alg["algorithm_id"])))
            self.table.setItem(i, 1, QTableWidgetItem(alg["name"]))
            self.table.setItem(i, 2, QTableWidgetItem(alg["type"]))
            self.table.setItem(i, 3, QTableWidgetItem(alg["parameters"]))
            self.table.setItem(i, 4, QTableWidgetItem(alg["created_at"]))
            self.table.setItem(i, 5, QTableWidgetItem(alg["updated_at"]))

        layout.addWidget(self.table)


        # Buton de revenire (în mod simplu se închide fereastra)
        self.btn_back = QPushButton("Back", self)
        self.btn_back.clicked.connect(self.close)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)
