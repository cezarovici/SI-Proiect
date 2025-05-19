# manage_keys.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor

class ManageKeysWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Keys")
        
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

        # Tabel pentru chei (exemplu: ID, Key Name, Algorithm)
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Key ID", 
            "Algorithm ID", 
            "Key Name", 
            "Key Value", 
            "Public Key", 
            "Private Key", 
            "Creation Date", 
            "Expiration Date", 
            "Is Active"
        ])

        # Exemplu de date modificate pentru a include toate câmpurile tabelei
        sample_keys = [
            {
                "key_id": 101, 
                "algorithm_id": 1, 
                "key_name": "AES Master Key", 
                "key_value": "fgh67dsh3k9d...", 
                "public_key": None, 
                "private_key": None, 
                "creation_date": "2025-05-20 00:00:00", 
                "expiration_date": "2026-05-20 00:00:00",
                "is_active": True
            },
            {
                "key_id": 102, 
                "algorithm_id": 2, 
                "key_name": "RSA Key Pair", 
                "key_value": None, 
                "public_key": "MIIBIjANBg...", 
                "private_key": "MIIEvQIBAD...", 
                "creation_date": "2025-05-20 00:00:00", 
                "expiration_date": "2027-05-20 00:00:00",
                "is_active": False
            }
        ]

        self.table.setRowCount(len(sample_keys))
        for i, key in enumerate(sample_keys):
            self.table.setItem(i, 0, QTableWidgetItem(str(key["key_id"])))
            self.table.setItem(i, 1, QTableWidgetItem(str(key["algorithm_id"])))
            self.table.setItem(i, 2, QTableWidgetItem(key["key_name"]))
            self.table.setItem(i, 3, QTableWidgetItem(key["key_value"] if key["key_value"] else "N/A"))
            self.table.setItem(i, 4, QTableWidgetItem(key["public_key"] if key["public_key"] else "N/A"))
            self.table.setItem(i, 5, QTableWidgetItem(key["private_key"] if key["private_key"] else "N/A"))
            self.table.setItem(i, 6, QTableWidgetItem(key["creation_date"]))
            self.table.setItem(i, 7, QTableWidgetItem(key["expiration_date"] if key["expiration_date"] else "N/A"))
            self.table.setItem(i, 8, QTableWidgetItem("Active" if key["is_active"] else "Inactive"))

        layout.addWidget(self.table)


        self.btn_back = QPushButton("Back", self)
        self.btn_back.clicked.connect(self.close)
        layout.addWidget(self.btn_back)

        self.btn_addkey = QPushButton("Add a key", self)
        layout.addWidget(self.btn_addkey)

        self.btn_deletekey = QPushButton("Delete a key", self)
        layout.addWidget(self.btn_deletekey)


        self.setLayout(layout)
