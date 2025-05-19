# manage_files.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor

class ManageFilesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Files")
        
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

        # Exemplu de date modificate pentru a include toate câmpurile tabelei
        sample_files = [
            {
                "file_id": 1, 
                "original_path": "/home/user/documents/file1.txt", 
                "encrypted_path": "/home/user/documents/file1.txt.enc", 
                "original_hash": "a4f5e2b6c3...", 
                "encrypted_hash": "b7c8d9e3f4...", 
                "algorithm_id": 1, 
                "key_id": 101, 
                "encryption_date": "2025-05-20 00:00:00", 
                "last_access": "2025-05-20 12:15:00"
            },
            {
                "file_id": 2, 
                "original_path": "/home/user/docs/file2.pdf", 
                "encrypted_path": "/home/user/docs/file2.pdf.enc", 
                "original_hash": "d2a7b9e5c4...", 
                "encrypted_hash": "e6f3g8h1i9...", 
                "algorithm_id": 2, 
                "key_id": 102, 
                "encryption_date": "2025-05-19 22:30:00", 
                "last_access": "2025-05-20 08:50:00"
            }
        ]

        self.table.setRowCount(len(sample_files))
        for i, file in enumerate(sample_files):
            self.table.setItem(i, 0, QTableWidgetItem(str(file["file_id"])))
            self.table.setItem(i, 1, QTableWidgetItem(file["original_path"]))
            self.table.setItem(i, 2, QTableWidgetItem(file["encrypted_path"]))
            self.table.setItem(i, 3, QTableWidgetItem(file["original_hash"] if file["original_hash"] else "N/A"))
            self.table.setItem(i, 4, QTableWidgetItem(file["encrypted_hash"] if file["encrypted_hash"] else "N/A"))
            self.table.setItem(i, 5, QTableWidgetItem(str(file["algorithm_id"])))
            self.table.setItem(i, 6, QTableWidgetItem(str(file["key_id"])))
            self.table.setItem(i, 7, QTableWidgetItem(file["encryption_date"]))
            self.table.setItem(i, 8, QTableWidgetItem(file["last_access"] if file["last_access"] else "N/A"))

        layout.addWidget(self.table)


        self.btn_back = QPushButton("Back", self)
        self.btn_back.clicked.connect(self.close)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)
